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
    targetDir = workingDir + "targets" + "/"
    imageDir = workingDir + "imaging_deep" + "/"

    SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", "config.cfg").replace(" ", "").split(",")]

    for id in SASidsTarget:
        parsetCalib = calibratorDir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
        configCalib = calibratorDir + str(id) + "_RAW/" + "pipeline.cfg"
        
        parsetTarget = targetDir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
        configTarget = targetDir + str(id) + "_RAW/" + "pipeline.cfg"
        
        os.system('genericpipeline.py '+ parsetCalib + ' -c ' +  configCalib + ' -d') # run calibrator
        os.system('genericpipeline.py '+ parsetTarget + ' -c ' +  configTarget + ' -d') # run target
        
    parsetImage = imageDir + "Initial-Subtract.parset"
    configImage = imageDir + "pipeline.cfg"
    os.system('genericpipeline.py '+ parsetImage + ' -c ' +  configImage + ' -d') # run imaging
