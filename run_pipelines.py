#!/usr/bin/env python3
import os
import sys
import argparse

from parsers._configparser import getConfigs


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Run pipelines. ''', epilog="""Pipelines""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


def run_pipeline(parset_file, config_file):
    try:
        os.system('genericpipeline.py ' + parset_file + ' -c ' + config_file + ' -d -v')
    except:
        print("Something went wrong")


def main():
    workingDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName",
                                                                                     "config.cfg") + "/"
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
        SASidsCalibrator = [int(id) for id in
                            getConfigs("Data", "calibratorSASids", "config.cfg").replace(" ", "").split(",")]

    if getConfigs("Operations", "which_obj", "config.cfg") == "all" or len(
            getConfigs("Operations", "which_obj", "config.cfg")) == 0:
        for id in SASidsCalibrator:
            parsetCalib = calibratorDir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
            configCalib = calibratorDir + str(id) + "_RAW/" + "pipeline.cfg"
            run_pipeline(parsetCalib, configCalib)  # run calibrator

        for id in SASidsTarget:
            parsetTarget = targetDir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
            configTarget = targetDir + str(id) + "_RAW/" + "pipeline.cfg"
            run_pipeline(parsetTarget, configTarget)  # run target

        parsetImage = imageDir + "Initial-Subtract.parset"
        configImage = imageDir + "pipeline.cfg"
        run_pipeline(parsetImage, configImage)  # run imaging

    elif getConfigs("Operations", "which_obj", "config.cfg") == "targets":

        for id in SASidsTarget:
            parsetTarget = targetDir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
            configTarget = targetDir + str(id) + "_RAW/" + "pipeline.cfg"
            run_pipeline(parsetTarget, configTarget)  # run target
    else:
        for id in SASidsCalibrator:
            parsetCalib = calibratorDir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
            configCalib = calibratorDir + str(id) + "_RAW/" + "pipeline.cfg"
            run_pipeline(parsetCalib, configCalib)  # run calibrator


if __name__ == "__main__":
    main()




