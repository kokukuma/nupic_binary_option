# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "timestamp",
      "fieldType": "datetime"
    },
    {
      "fieldName": "open",
      "fieldType": "float",
      "maxValue": 150.0,
      "minValue": 90.0
    },
    {
      "fieldName": "high",
      "fieldType": "float",
      "maxValue": 150.0,
      "minValue": 90.0
    },
    {
      "fieldName": "low",
      "fieldType": "float",
      "maxValue": 150.0,
      "minValue": 90.0
    },
    {
      "fieldName": "close",
      "fieldType": "float",
      "maxValue": 150.0,
      "minValue": 90.0
    },
  ],
  "streamDef": {
    "info": "binary_option",
    "version": 1,
    "streams": [
      {
        "info": "binary option",
        "source": "file://datasets/usdjpy_2001_01_ohlc.csv",
        #"source": "file://datasets/usdjpy_2001_2005_ohlc.csv",
        #"source": "file://datasets/usdjpy_2001_ohlc.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },
  "inferenceType": "TemporalAnomaly",
  "inferenceArgs": {
    "predictionSteps": [
      24
    ],
    "predictedField": "low",
  },
  "iterationCount": 20,
  "maxModels": 10,
  "swarmSize": "small"
}
