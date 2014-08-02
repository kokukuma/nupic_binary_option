MODEL_PARAMS = \
{ 'aggregationInfo': { 'days': 0,
                       'fields': [],
                       'hours': 0,
                       'microseconds': 0,
                       'milliseconds': 0,
                       'minutes': 0,
                       'months': 0,
                       'seconds': 0,
                       'weeks': 0,
                       'years': 0},
  'model': 'CLA',
  'modelParams': { 'anomalyParams': { u'anomalyCacheRecords': None,
                                      u'autoDetectThreshold': None,
                                      u'autoDetectWaitRecords': None},
                   'clParams': { 'alpha': 0.005,
                                 'clVerbosity': 0,
                                 'regionName': 'CLAClassifierRegion',
                                 'steps': '1,4,24'},
                   'inferenceType': 'TemporalAnomaly',
                   'sensorParams': { 'encoders': {
                                                   # u'open': { 'clipInput': True,
                                                   #           'fieldname': 'open',
                                                   #           'maxval': 150.0,
                                                   #           'minval': 90.0,
                                                   #           'n': 100,
                                                   #           'name': 'low',
                                                   #           'type': 'ScalarEncoder',
                                                   #           'w': 21},
                                                   # u'high': { 'clipInput': True,
                                                   #            'fieldname': 'high',
                                                   #            'maxval': 150.0,
                                                   #            'minval': 90.0,
                                                   #            'n': 100,
                                                   #            'name': 'high',
                                                   #            'type': 'ScalarEncoder',
                                                   #            'w': 21},
                                                   # u'close': { 'clipInput': True,
                                                   #           'fieldname': 'close',
                                                   #           'maxval': 150.0,
                                                   #           'minval': 90.0,
                                                   #           'n': 100,
                                                   #           'name': 'low',
                                                   #           'type': 'ScalarEncoder',
                                                   #           'w': 21},
                                                   u'low': { 'clipInput': True,
                                                             'fieldname': 'low',
                                                             'maxval': 200.0,
                                                             'minval': 0.0,
                                                             'name': 'low',
                                                             'type': 'DeltaEncoder',
                                                             # 'n': 23,
                                                             # 'w': 21
                                                             'n': 1000,
                                                             'w': 21
                                                             # 'n': 3000,
                                                             # 'w': 31
                                                             },
                                                   # u'low': { 'clipInput': True,
                                                   #           'fieldname': 'low',
                                                   #           'maxval': 200.0,
                                                   #           'minval': 0.0,
                                                   #           'name': 'low',
                                                   #           'type': 'ScalarEncoder',
                                                   #           # 'n': 23,
                                                   #           # 'w': 21
                                                   #           'n': 500,
                                                   #           'w': 21
                                                   #           # 'n': 3000,
                                                   #           # 'w': 31
                                                   #           },
                                                   u'open': None,
                                                   u'high': None,
                                                   u'close': None,
                                                   #u'low': None,
                                                   # u'flg': { 'clipInput': True,
                                                   #           'fieldname': 'flg',
                                                   #           'maxval': 1.0,
                                                   #           'minval': 0.0,
                                                   #           'n': 63,
                                                   #           'name': 'flg',
                                                   #           'type': 'ScalarEncoder',
                                                   #           'w': 21},
                                                   # u'_classifierInput': { 'clipInput': True,
                                                   #           'classifierOnly': True,
                                                   #           'fieldname': 'low',
                                                   #           'maxval': 150.0,
                                                   #           'minval': 90.0,
                                                   #           'n': 23,
                                                   #           #'name': 'low',
                                                   #           'name': '_classifierInput',
                                                   #           'type': 'ScalarEncoder',
                                                   #           'w': 21},
                                                   u'timestamp_dayOfWeek': None,
                                                   u'timestamp_timeOfDay': None,
                                                   # u'timestamp_timeOfDay': { 'fieldname': 'timestamp',
                                                   #                           'name': 'timestamp',
                                                   #                           'timeOfDay': ( 21,
                                                   #                                          1.0024781365542386),
                                                   #                           'type': 'DateEncoder'},
                                                   u'timestamp_weekend': None},
                                     'sensorAutoReset': None,
                                     'verbosity': 0},
                   'spEnable': True,
                   'spParams': { 'columnCount': 2048,
                                 'globalInhibition': 1,
                                 'inputWidth': 0,
                                 'maxBoost': 2.0,
                                 'numActiveColumnsPerInhArea': 20,
                                 'potentialPct': 0.8,
                                 #'potentialPct': 1.0,
                                 #'potentialPct': 0.3,
                                 'seed': 1956,
                                 'spVerbosity': 0,
                                 'spatialImp': 'cpp',
                                 'synPermActiveInc': 0.05,
                                 'synPermConnected': 0.1,
                                 'synPermInactiveDec': 0.09},
                   'tpEnable': True,
                   'tpParams': { 'activationThreshold': 14,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'globalDecay': 0.0,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'maxAge': 0,
                                 'maxSegmentsPerCell': 128,
                                 'maxSynapsesPerSegment': 32,
                                 'minThreshold': 10,
                                 'newSynapseCount': 20,
                                 'outputType': 'normal',
                                 #'outputType': 'activeState',
                                 #'outputType': 'activeState1CellPerCol',
                                 'pamLength': 1,
                                 #'burnIn': 1,
                                 # 'connectedPerm': 0.5,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1960,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0},
                   'trainSPNetOnlyIfRequested': False},
  'predictAheadTime': None,
  'version': 1}
