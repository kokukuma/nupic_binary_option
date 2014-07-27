#!/usr/bin/python
# coding: utf-8


import os
import csv
import numpy
import datetime
from collections import defaultdict

DATETIME_FORMAT = "%Y%m%d%H%M%S"

def main():
    """
    convert USDJPY.txt to swarm_input.csv

    <TICKER>,<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
    USDJPY,20010102,230300,114.43,114.43,114.43,114.43,4
    USDJPY,20010102,230400,114.44,114.44,114.44,114.44,4

    """
    csv_file_name = 'usdjpy_2001_01.csv'
    start_time = datetime.datetime.strptime("20010102230300", DATETIME_FORMAT)
    end_time   = datetime.datetime.strptime("20020102230300", DATETIME_FORMAT)

    # csv_file_name = 'usdjpy_2001_2005.csv'
    # start_time = datetime.datetime.strptime("20010102230300", DATETIME_FORMAT)
    # end_time   = datetime.datetime.strptime("20060102230300", DATETIME_FORMAT)

    # csv_file_name = 'usdjpy_2006_2007.csv'
    # start_time = datetime.datetime.strptime("20060102230300", DATETIME_FORMAT)
    # end_time   = datetime.datetime.strptime("20080102230300", DATETIME_FORMAT)


    # 分単位だとちょっと小さすぎるから時間単位に変換する.
    print 'Reading ...'
    with open('USDJPY.txt', "rb") as f:
        csvReader = csv.reader(f)
        csvReader.next()

        date_h_data = defaultdict(list)
        for row in csvReader:
            timestamp = datetime.datetime.strptime(row[1]+row[2], DATETIME_FORMAT)

            if start_time > timestamp:
                continue
            if end_time < timestamp:
                break
            date_h  = datetime.datetime.strftime(timestamp, "%Y%m%d%H")
            date_h_data[date_h].append([row[4], row[5]])


    # 時間の中でhigh/lowを取り出す.
    print 'Converting ...'
    csv_data = []
    for date_h, data in date_h_data.items():
        high_list = numpy.array(data)[:,0]
        low_list  = numpy.array(data)[:,1]
        timestamp = datetime.datetime.strptime(date_h, "%Y%m%d%H")
        csv_data.append([timestamp, max(high_list), min(low_list)])


    # csvに保存
    with open(csv_file_name, 'wb') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(['timestamp', 'high', 'low'])
        csvWriter.writerow(['datetime', 'float', 'float'])
        csvWriter.writerow(['T', '', ''])
        for d in sorted(csv_data):
            print d[0], d[1], d[2]
            csvWriter.writerow(d)

if __name__ == "__main__":
    main()
