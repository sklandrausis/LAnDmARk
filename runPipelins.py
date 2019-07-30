import os
import sys
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

def run_pipeline(parset_file, config_file):
    try:
        os.system('genericpipeline.py ' + parset_file + ' -c ' + config_file + ' -d')
    except:
        print("Something went wrong")

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

        run_pipeline(parsetCalib, configCalib) # run calibrator
        run_pipeline(parsetCalib, configTarget) # run target

    for id in SASidsTarget:
        dir_from = targetDir + str(id) + "_RESULTS/results/*.ms"
        dir_to = workingDir + image_input + "/"

        os.system("cp -rvf " + dir_from + " " + dir_to)

    parsetImage = imageDir + "Prefactor-Image.parset"
    configImage = imageDir + "pipeline.cfg"
    run_pipeline(parsetImage, configImage) # run imaging
    sys.exit(0)
