''' Executes all scripts '''
import os
import sys
import time
import argparse

from parsers._configparser import getConfigs

try:
    import coloredlogs
except ImportError:
    print('coloredlogs module is not installed')
    sys.exit(1)

try:
    import awlofar
except ImportError:
    print('awlofar module is not installed')
    sys.exit(1)

try:
    import matplotlib
except ImportError:
    print('matplotlib module is not installed')
    sys.exit(1)

try:
    import numpy
except ImportError:
    print('numpy module is not installed')
    sys.exit(1)

try:
    import seaborn
except ImportError:
    print('seaborn module is not installed')
    sys.exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Executes all scripts. ''', epilog="""Main""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-d", "--print_logs", help="Print log", action="store_true", default=False)
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


if __name__ == "__main__":

    start_time_main = time.time()

    config_file = get_args("config")

    if getConfigs("Operations", "querying", config_file) == "True":
        if get_args("print_logs") == "True":
            os.system("python3 " + "selectionStaging.py -d")
        else:
            os.system("python3 " + "selectionStaging.py")

    if getConfigs("Operations", "Retrieve", config_file) == "True":
        start_data_retrive_time = time.time()
        os.system("python3 " + "retrieveDataproducts.py")
        end_data_retrive_time = time.time()
        print("Data selection time", end_data_retrive_time  - start_data_retrive_time)

    if getConfigs("Operations", "Process", config_file) == "True":
        start_data_process_time = time.time()
        os.system("python3 " + "runPipelines.py")
        end_data_process_time = time.time()
        print("Data download time", end_data_process_time - start_data_process_time)

    end_time_main = time.time()
    print("Total time ", end_time_main - start_time_main)
