#!/usr/bin/python

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

    def reset(self):
        self.ok_count = 0
        self.ng_count = 0

    def evaluate(self, before, now, high_pred, low_pred):
        # high/low predict
        if  before< low_pred:
            pred = 'high'
        elif  before > high_pred:
            pred = 'low'
        else:
            pred = 'not'

        # evalueate
        green = '\033[32m'
        yellow= '\033[33m'
        red   = '\033[31m'
        clear = '\033[0m'

        res = 'high' if now - before > 0 else 'low'
        if pred == 'not':
            evalue = yellow + 'NO' + clear
        elif res == pred:
            evalue = green + 'OK' + clear
            self.ok_count += 1
        else:
            evalue = red + 'NG' + clear
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
    high_value = float(row[1])
    low_value  = float(row[2])
    now_value = (high_value + low_value)/2
    return timestamp, high_value, low_value, now_value

def runModel(inputFilePath, high_model, low_model, print_result=True):

    csv_data = get_csv_data(inputFilePath)
    ep = Evaluate()
    if print_result:
        output = nupic_output.NuPICPlotOutput(["Binary Option"])
        shifter = InferenceShifter()
        shifter2 = InferenceShifter()

    counter = 0
    before_value = None
    for row in csv_data:
        counter += 1
        if (counter % 1800 == 0) :
            print timestamp,
            print "Read %i lines..." % counter
            ep.reset()

        timestamp, high_value, low_value, now_value = get_formated_data(row)

        # run cla model
        high_result = high_model.run({
            "timestamp": timestamp,
            "high": high_value,
            "low": low_value
        })
        low_result = low_model.run({
            "timestamp": timestamp,
            "high": high_value,
            "low": low_value
        })

        if print_result:
            # print prediction
            high_result = shifter.shift(high_result)
            high_prediction = high_result.inferences["multiStepBestPredictions"][1]
            anomalyScore = high_result.inferences["anomalyScore"]
            output.write(timestamp, high_value, high_prediction, anomalyScore)

            # print prediction
            low_result = shifter2.shift(low_result)
            low_prediction = low_result.inferences["multiStepBestPredictions"][1]

            # evaluate high/low
            if before_value:
                ep.evaluate(before_value, now_value, high_prediction, low_prediction)

            # save now_value
            before_value = now_value

    if print_result:
        output.close()


def binary_option():
    #inputFilePath = "./datasets/usdjpy_2001_01.csv"
    inputFilePath = "./datasets/usdjpy_2001_2005.csv"
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
