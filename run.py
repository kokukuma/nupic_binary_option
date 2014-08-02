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

from model_params import model_params

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

    def __init__(self, number=1):
        self.number = number
        self.ok_count = [0 for i in range(self.number)]
        self.ng_count = [0 for i in range(self.number)]
        self.color = { 'green': '\033[32m',
                       'yellow': '\033[33m',
                       'red': '\033[31m',
                       'clear': '\033[0m'}

    def reset(self):
        self.ok_count = [0 for i in range(self.number)]
        self.ng_count = [0 for i in range(self.number)]

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
                self.ok_count[i] += 1
            else:
                evalue = self.color['red'] + 'NG' + self.color['clear']
                self.ng_count[i] += 1

            ok_rate = float(self.ok_count[i])/(self.ok_count[i] + self.ng_count[i])
            print "%5s, %10s, %5.4f" % (pred, evalue, ok_rate) ,
        print


    # TODO: 現状動かなくなっているから直す.
    def evaluate(self, before, now, high_pred, low_pred):
        """
        2パラメータによるhigh/low予測

        high/low値の予測を想定
         predict_list = [(high, low), (high, low)....]
        """
        res = 'high' if now - before > 0 else 'low'
        print "%5.2f -> %5.2f, %5s, " % (before, now, res) ,

        for i, pred_data in enumerate(predict_list):
            # high/low predict
            if  before< pred_data[1]:
                pred = 'high'
            elif  before > pred_data[0]:
                pred = 'low'
            else:
                pred = 'not'

            # evalueate
            if pred == 'not':
                evalue = self.color['yellow'] + 'NO' + self.color['clear']
            elif res == pred:
                evalue = self.color['green'] + 'OK' + self.color['clear']
                self.ok_count[i] += 1
            else:
                evalue = self.color['red'] + 'NG' + self.color['clear']
                self.ng_count[i] += 1

            if pred == 'not':
                print "%5s, %10s" % (pred, evalue)
            else:
                ok_rate = float(self.ok_count[i])/(self.ok_count[i] + self.ng_count[i])
                print "%5s, %10s, %5.4f" % (pred, evalue, ok_rate)
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
    now_value = (high_value + low_value)/2

    return {'timestamp': timestamp,
            # 'open': open_value,
            # 'high': high_value,
            'low': low_value,
            # 'close': close_value,
            } , now_value

def runModel(inputFilePath, high_model, low_model, print_result=True):

    ep = Evaluate(number=3)
    region_sate = RegionState()

    csv_data = get_csv_data(inputFilePath)

    if print_result:
        #output = nupic_output.NuPICPlotOutput(["Binary Option"])
        output = nupic_output.NuPICFileOutput("Binar Option")
        shifter_high = InferenceShifter()
        shifter_low = InferenceShifter()

    counter = 0
    before_value = None
    before_predvalue = []

    for i in range(1):
        for row in csv_data:
            counter += 1
            if (counter % 720 == 0) :
                print i, data['timestamp'],
                print "Read %i lines..." % counter
                ep.reset()      # high/low予測結果のリセット.
                counter = 0

            data, now_value = get_formated_data(row)

            # run cla model
            #high_result = high_model.run(data)
            low_result = low_model.run(data)

            region_sate.save(data['low'], low_model, low_result)


            # TODO: この辺網ちょっと綺麗に修正する.
            if print_result:
                # # high prediction
                # high_result = shifter_high.shift(high_result)
                # high_prediction = high_result.inferences["multiStepBestPredictions"][1]

                # low prediction
                low_result = shifter_low.shift(low_result)
                low_prediction    = low_result.inferences["multiStepBestPredictions"][1]
                low_prediction_4  = low_result.inferences["multiStepBestPredictions"][4]
                low_prediction_24 = low_result.inferences["multiStepBestPredictions"][24]

                # print graph
                anomalyScore = low_result.inferences["anomalyScore"]
                output.write(data['timestamp'], data['low'], low_prediction, anomalyScore)

                # evaluate high/low
                if before_value:
                    print i,counter,
                    ep.evaluate_one(before_value, data['low'], [low_prediction, low_prediction_4, low_prediction_24], before_predvalue)

                # save now_value
                #before_value = now_value
                # TODO: ここ間違ってる. low_prediction_4は４時間前, low_prediction_24は24時間前のものが必要.
                # InferenceShifter を上手く使えるかな?
                before_value     = data['low']
                before_predvalue = [low_prediction, low_prediction_4, low_prediction_24]

    region_sate.show(low_model)


    if print_result:
        output.close()


def binary_option():
    inputFilePath = "./datasets/usdjpy_2001_01_ohlc.csv"
    #inputFilePath = "./datasets/usdjpy_2001_ohlc.csv"
    #inputFilePath = "./datasets/usdjpy_2001_2005_ohlc.csv"
    #inputFilePath = "./datasets/usdjpy_2006_2007.csv"

    print 'create model ...'
    high_model = createModel("high")
    low_model  = createModel("low")

    # TODO: 学習したモデルの保存ができてない.
    # if os.path.exists('./learned_model'):
    #     high_model.load('./learned_model/high/')
    #     low_model.load('./learned_model/low/')


    print 'run Model ...'
    runModel(inputFilePath, high_model, low_model, True)

    # TODO: 学習したモデルの保存ができてない.
    # print 'pickle dump ...'
    # high_model.save(os.path.abspath('./learned_model/high/'))
    # low_model.save(os.path.abspath('./learned_model/low/'))


if __name__ == "__main__":
    binary_option()
