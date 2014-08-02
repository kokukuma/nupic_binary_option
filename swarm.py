#!/usr/bin/python

import os
import pprint

from nupic.swarming import permutations_runner
from swarm_description import SWARM_DESCRIPTION


def writeModelParams(modelParams):
    outDir = os.path.join(os.getcwd(), 'model_params')
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    #outPath = os.path.join(outDir, "model_params.py")
    outPath = os.path.join(outDir, "tmp.py")

    pp = pprint.PrettyPrinter(indent=2)

    with open(outPath, "wb") as outFile:
        modelParamsString = pp.pformat(modelParams)
        outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
    return outPath

def swarm():
    swarmWorkDir = os.path.abspath("swarm")
    if not os.path.exists(swarmWorkDir):
        os.mkdir(swarmWorkDir)
    print swarmWorkDir
    modelParams = permutations_runner.runWithConfig(
            SWARM_DESCRIPTION,
            {"maxWorkers": 4, "overwrite": True},
            outputLabel="rec_center",
            outDir=swarmWorkDir,
            permWorkDir=swarmWorkDir
            )
    writeModelParams(modelParams)

if __name__ == "__main__":
    swarm()


