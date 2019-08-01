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
    project = getConfigs("Data", "PROJECTid", "config.cfg")

    if len(getConfigs("Data", "calibratorSASids", "config.cfg")) == 0:
        if project == "MSSS_HBA_2013":
            SASidsCalibrator = [id - 1 for id in SASidsTarget]

        else:
            raise Exception("SAS id for calibrator is not set in config.cfg file")
            sys.exit(1)
    else:
        SASidsCalibrator =  [int(id) for id in getConfigs("Data", "calibratorSASids", "config.cfg").replace(" ", "").split(",")]

    for id in SASidsCalibrator:
        parsetCalib = calibratorDir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
        configCalib = calibratorDir + str(id) + "_RAW/" + "pipeline.cfg"
        run_pipeline(parsetCalib, configCalib)  # run calibrator

    for id in SASidsTarget:
        parsetTarget = targetDir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
        configTarget = targetDir + str(id) + "_RAW/" + "pipeline.cfg"
        run_pipeline(parsetTarget, configTarget) # run target

    for id in SASidsTarget:
        dir_from = targetDir + str(id) + "_RESULTS/results/*.ms"
        dir_to = workingDir + "image_input/"
        os.system("cp -rvf " + dir_from + " " + dir_to)

    parsetImage = imageDir + "Prefactor-Image.parset"
    configImage = imageDir + "pipeline.cfg"
    run_pipeline(parsetImage, configImage) # run imaging
    sys.exit(0)
