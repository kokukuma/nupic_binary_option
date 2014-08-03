#!/usr/bin/python
# coding: utf-8

import os
import csv
import datetime
import pickle
from pprint import pprint

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.clamodel import CLAModel
import nupic_output
import nupic_anomaly_output as nupic_output

from model_params import model_params_direct as model_params

from collections import defaultdict


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class RegionState(object):
    """
    debuga用: モデルの状態を保存しておく.
    """
    def __init__(self):
        self.bucket_dict = defaultdict(set)
        self.encoder_dict = defaultdict(set)
        self.spacial_dict = defaultdict(set)
        self.temporal_dict = defaultdict(set)


    def save(self, input_value, model, low_result):

        # sensor output
        sensor = model._getSensorRegion()
        sensorOutput = sensor.getOutputData('dataOut')
        patternNZ = sensorOutput.nonzero()[0]
        #print patternNZ.tolist()

        self.encoder_dict[input_value] = patternNZ.tolist()

        # sp output
        sp = model._getSPRegion()
        spOutput = sp.getOutputData('bottomUpOut')
        patternNZ = spOutput.nonzero()[0]

        self.spacial_dict[input_value] = patternNZ.tolist()

        self.temporal_dict[input_value] = low_result.inferences['multiStepPredictions'][1]

        # tp output
        tp = model._getTPRegion()
        tpOutput = tp.getSelf()._tfdr.infActiveState['t']
        patternNZ = tpOutput.reshape(-1).nonzero()[0]
        #print patternNZ

        # classifier = model._getClassifierRegion()
        # print classifier
        # print classifier._claClassifier._activeBitHistory[(2112, 1)]._stats
        #

    def show(self, model):
        print
        print 'Bucket'
        for input_value, _ in sorted(self.encoder_dict.items(), key=lambda x:x[0]):
            bucket_id = model._classifierInputEncoder.getBucketIndices(input_value)[0]
            self.bucket_dict[bucket_id].add(input_value)
        for bucket_id , input_values in self.bucket_dict.items():
            print len(input_values), bucket_id

        print
        print 'Enc'

        encoder_pattern = defaultdict(set)
        for input_value, pattern in self.encoder_dict.items():
            encoder_pattern[tuple(pattern)].add(input_value)
        for key,value in encoder_pattern.items():
            print len(value), value
        print
        print 'SP'
        spacial_pattern = defaultdict(set)
        for key, value in self.spacial_dict.items():
            spacial_pattern[tuple(value)].add(key)
        for key,value in spacial_pattern.items():
            print len(value), value
        print
        print 'predict'
        for key, value in sorted(self.temporal_dict.items(), key=lambda x:x[0]):
            print key, len(value), value.keys()




class Evaluate(object):
    """
    high/low評価用
    """

    def __init__(self, predict_number=1):
        self.number = predict_number
        self.color = { 'green': '\033[32m',
                       'yellow': '\033[33m',
                       'red': '\033[31m',
                       'clear': '\033[0m'}

        self.rate_slice    = 720 # 30日

        self.ok_ng = []
        self.result = defaultdict(list)

    # def reset(self):
    #     self.ok_count = [0 for i in range(self.number)]
    #     self.ng_count = [0 for i in range(self.number)]


    def evaluate_high_low(self, data, predict, anomalyScore):
        """
        high/lowを直接予測した場合.
        """
        #anomaly_limit = 0.2
        anomaly_limit = 1.0

        if anomalyScore > anomaly_limit:
            evalue = self.color['green'] + 'NO' + self.color['clear']
        elif data['high_low'] == predict:
            evalue = self.color['green'] + 'OK' + self.color['clear']
            self.ok_ng.append(1)
        else:
            evalue = self.color['red'] + 'NG' + self.color['clear']
            self.ok_ng.append(0)

        if anomalyScore > anomaly_limit:
            print "%10s, %5s, %10s" % (data['timestamp'], predict, evalue)
        else:
            ok_rate = float(sum(self.ok_ng[-self.rate_slice:]))/(len(self.ok_ng[-self.rate_slice:])+1)
            print "%10s, %5s, %10s, %5.4f, %5.4f" % (data['timestamp'], predict, evalue, ok_rate, anomalyScore)

        self.ok_ng = self.ok_ng[-self.rate_slice:]


    def evaluate_one(self, before, now, predict_list, before_predvalue):
        """
        1パラメータによるhigh/low予測

        close値のみの予測を想定.

        predict_list = [value, value, value...]
        """
        res  = 'high' if now > before  else 'low'

        print "%5.2f -> %5.2f, %5s, " % (before, now, res) ,
        for i, p_val in enumerate(predict_list):
            pred = 'high' if p_val > before_predvalue[i] else 'low'

            if res == pred:
                evalue = self.color['green'] + 'OK' + self.color['clear']
                self.result[i].append(1)
            else:
                evalue = self.color['red'] + 'NG' + self.color['clear']
                self.result[i].append(0)

            ok_rate = float(sum(self.result[i][-self.rate_slice:]))/(len(self.result[i][-self.rate_slice:])+1)
            print "%5s, %10s, %5.4f" % (pred, evalue, ok_rate) ,

            self.result[i] = self.result[i][-self.rate_slice:]
        print


def createModel(target):
    model = ModelFactory.create(model_params.MODEL_PARAMS)
    model.enableInference({
        "predictedField": target
        })
    return model

def get_csv_data(inputFilePath):
    data = []
    with open(inputFilePath, "rb") as inputFile:
        csvReader = csv.reader(inputFile)
        # skip header rows
        csvReader.next()
        csvReader.next()
        csvReader.next()
        for row in csvReader:
            data.append(row)
    return data

def get_formated_data(row):
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    open_value = float(row[1])
    high_value = float(row[2])
    low_value  = float(row[3])
    close_value  = float(row[4])

    return {'timestamp': timestamp,
            'open': open_value,
            'high': high_value,
            'low': low_value,
            'high_low': 'none',
            'close': close_value,
            }

def runModel(inputFilePath, low_model):

    ep = Evaluate(predict_number=3)
    region_sate = RegionState()

    csv_data = get_csv_data(inputFilePath)

    shifter_high = InferenceShifter()
    shifter_low = InferenceShifter()

    counter = 0
    before_value = None
    before_predvalue = []

    for i in range(2):
        for row in csv_data:
            counter += 1
            if (counter % 10 == 0) :
                tp = low_model._getTPRegion()
                tp.getSelf().resetSequenceStates()

            # data準備
            data = get_formated_data(row)
            if before_value:
                data['high_low'] = 'high' if before_value < data['low'] else 'low'

            # run cla model
            low_result = low_model.run(data)
            #region_sate.save(data['low'], low_model, low_result)

            # low prediction
            low_result      = shifter_low.shift(low_result)
            high_low_prediction  = low_result.inferences["multiStepBestPredictions"][1]
            anomalyScore    = low_result.inferences["anomalyScore"]

            # # evaluate high/low
            if before_value:
                print i,counter,
                ep.evaluate_high_low(data, high_low_prediction, anomalyScore)

            # save now_value
            # TODO: InferenceShifter を上手く使った方法に変更したい.
            before_value     = data['low']

    # region_sate.show(low_model)

    return low_model

def binary_option():
    from nupic.frameworks.opf.model import Model

    #inputFilePath = "./datasets/usdjpy_2001_01_ohlc.csv"
    # inputFilePath = "./datasets/usdjpy_2001_ohlc.csv"
    #inputFilePath = "./datasets/usdjpy_2001_2005_ohlc.csv"
    inputFilePath = "./datasets/usdjpy_2006_2007.csv"


    # predict_mode: disableLearning and dont save the model
    predict_mode = True

    if os.path.exists('./learned_model_direct'):
        print 'read learned_model'
        low_model  = Model.load('./learned_model_direct/low/')
        if predict_mode:
            low_model.disableLearning()
        else:
            low_model.enableLearning()

    else:
        print 'create model ...'
        low_model  = createModel("high_low")

    print 'run Model ...'
    low_model = runModel(inputFilePath, low_model)

    if not predict_mode:
        print 'pickle dump ...'
        low_model.save(os.path.abspath('./learned_model_direct/low/'))


if __name__ == "__main__":
    binary_option()
