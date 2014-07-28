#!/usr/bin/python
# coding: utf-8

import os
import csv
import datetime
import pickle

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.clamodel import CLAModel
import nupic_output
import nupic_anomaly_output as nupic_output

from model_params import model_params

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def createModel(target):
    model = ModelFactory.create(model_params.MODEL_PARAMS)
    model.enableInference({
        "predictedField": target
        })
    return model

class Evaluate(object):

    def __init__(self):
        self.ok_count = 0
        self.ng_count = 0
        self.color = { 'green': '\033[32m',
                       'yellow': '\033[33m',
                       'red': '\033[31m',
                       'clear': '\033[0m'}

    def reset(self):
        self.ok_count = 0
        self.ng_count = 0

    def evaluate_one(self, before, now, predict):
        """
        close値のみの予測を想定
        """
        pred = 'high' if predict > before else 'low'
        res  = 'high' if now > before  else 'low'

        if pred == 'not':
            evalue = self.color['yellow'] + 'NO' + self.color['clear']
        elif res == pred:
            evalue = self.color['green'] + 'OK' + self.color['clear']
            self.ok_count += 1
        else:
            evalue = self.color['red'] + 'NG' + self.color['clear']
            self.ng_count += 1

        if pred == 'not':
            print "%5.2f -> %5.2f, %5s, %5s, %10s" % (before, now, res, pred, evalue)
        else:
            ok_rate = float(self.ok_count)/(self.ok_count + self.ng_count)
            print "%5.2f -> %5.2f, %5s, %5s, %10s, %5.4f" % (before, now, res, pred, evalue, ok_rate)


    def evaluate(self, before, now, high_pred, low_pred):
        """
        high/low値の予測を想定
        """
        # high/low predict
        if  before< low_pred:
            pred = 'high'
        elif  before > high_pred:
            pred = 'low'
        else:
            pred = 'not'

        # evalueate

        res = 'high' if now - before > 0 else 'low'
        if pred == 'not':
            evalue = self.color['yellow'] + 'NO' + self.color['clear']
        elif res == pred:
            evalue = self.color['green'] + 'OK' + self.color['clear']
            self.ok_count += 1
        else:
            evalue = self.color['red'] + 'NG' + self.color['clear']
            self.ng_count += 1

        if pred == 'not':
            print "%5.2f -> %5.2f, %5s, %5s, %10s" % (before, now, res, pred, evalue)
        else:
            ok_rate = float(self.ok_count)/(self.ok_count + self.ng_count)
            print "%5.2f -> %5.2f, %5s, %5s, %10s, %5.4f" % (before, now, res, pred, evalue, ok_rate)

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
    #return (timestamp, open_value, high_value, low_value, close_value,now_value)

    return {'timestamp': timestamp,
            'open': open_value,
            'high': high_value,
            'low': low_value,
            'close': close_value,
            } , now_value

def runModel(inputFilePath, high_model, low_model, print_result=True):

    csv_data = get_csv_data(inputFilePath)
    ep = Evaluate()
    if print_result:
        output = nupic_output.NuPICPlotOutput(["Binary Option"])
        shifter = InferenceShifter()
        shifter2 = InferenceShifter()

    counter = 0
    before_value = None
    for i in range(10):
        for row in csv_data:
            counter += 1
            if (counter % 720 == 0) :
                print i, data['timestamp'],
                print "Read %i lines..." % counter
                ep.reset()

            data, now_value = get_formated_data(row)

            # run cla model
            high_result = high_model.run(data)
            low_result = low_model.run(data)

            if print_result:
                # print prediction
                high_result = shifter.shift(high_result)
                high_prediction = high_result.inferences["multiStepBestPredictions"][1]
                anomalyScore = high_result.inferences["anomalyScore"]
                output.write(data['timestamp'], data['high'], high_prediction, anomalyScore)

                # print prediction
                low_result = shifter2.shift(low_result)
                low_prediction = low_result.inferences["multiStepBestPredictions"][1]

                # evaluate high/low
                if before_value:
                    print i,counter,
                    ep.evaluate(before_value, now_value, high_prediction, low_prediction)

                # save now_value
                before_value = now_value

    if print_result:
        output.close()


def binary_option():
    inputFilePath = "./datasets/usdjpy_2001_ohlc.csv"
    #inputFilePath = "./datasets/usdjpy_2001_2005_ohlc.csv"
    #inputFilePath = "./datasets/usdjpy_2006_2007.csv"

    print 'create model ...'
    high_model = createModel("high")
    low_model  = createModel("low")
    if os.path.exists('./learned_model'):
        high_model.load('./learned_model/high/')

        low_model.load('./learned_model/low/')


    print 'run Model ...'
    runModel( inputFilePath, high_model, low_model, True)

    print 'pickle dump ...'
    high_model.save(os.path.abspath('./learned_model/high/'))
    low_model.save(os.path.abspath('./learned_model/low/'))


if __name__ == "__main__":
    binary_option()
