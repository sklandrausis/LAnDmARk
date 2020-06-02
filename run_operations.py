#!/usr/bin/env python3
import sys
from sys import version_info
import os
import argparse
from services.querying_service import Querying
from parsers._configparser import getConfigs


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Run selected operations. ''')
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


config_file = get_args("config")

SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")]
project = getConfigs("Data", "PROJECTid", config_file)

if len(getConfigs("Data", "calibratorSASids", config_file)) == 0:
    if project == "MSSS_HBA_2013":
        SASidsCalibrator = [id - 1 for id in SASidsTarget]

    else:
        raise Exception("SAS id for calibrator is not set in config.cfg file")
else:
    SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", config_file).replace(" ", "").split(",")]


def query():

    if getConfigs("Operations", "which_obj",  config_file) == "calibrators":
        q1 = Querying(SASidsCalibrator, True, config_file)
        q2 = None
    elif getConfigs("Operations", "which_obj",  config_file) == "target":
        q1 = None
        q2 = Querying(SASidsTarget, False, config_file)
    else:
        q1 = Querying(SASidsCalibrator, True, config_file)
        q2 = Querying(SASidsTarget, False, config_file)
    return q1, q2


def main():
    q1, q2 = query()
    if getConfigs("Operations", "querying", config_file) == "True":
        querying_results = open("querying_results.txt", "w")

        if q1 is None:
            msg_st = q2.get_station_count_message()
            querying_results.write(msg_st)
            querying_results.write("\n")
            msg_d = q2.get_valid_file_message()
            querying_results.write(msg_d)
            querying_results.write("\n")
        elif q2 is None:
            msg_st = q1.get_station_count_message()
            querying_results.write(msg_st)
            querying_results.write("\n")
            msg_d = q1.get_valid_file_message()
            querying_results.write(msg_d)
            querying_results.write("\n")
        else:
            msg1_st = q1.get_station_count_message()
            msg2_st = q2.get_station_count_message()
            msg_st = msg1_st + "\n" + msg2_st
            querying_results.write(msg_st)
            querying_results.write("\n")
            msg1_d = q1.get_valid_file_message()
            msg2_d = q2.get_valid_file_message()
            msg_d = msg1_d + "\n" + msg2_d
            querying_results.write(msg_d)
            querying_results.write("\n")

        querying_results.write("done")
        querying_results.close()









    sys.exit(0)


if __name__ == "__main__":
    main()
