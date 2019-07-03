import os
import argparse

from parsers._configparser import getConfigs

def parseArguments():
    parser = argparse.ArgumentParser(description='''Run pipelines. ''', epilog="""Pipelines""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args

def getArgs(key):
    return str(parseArguments().__dict__[key])

if __name__ == "__main__":
    workingDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/"
    calibratorDir = workingDir + "calibrators" + "/"

    SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", "config.cfg").replace(" ", "").split(",")]

    for id in SASidsTarget:
        parset = calibratorDir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
        config = calibratorDir + str(id) + "_RAW/" + "pipeline.cfg"

        os.system('genericpipeline.py '+ parset + ' -c ' +  config + ' -d') # run calibrator