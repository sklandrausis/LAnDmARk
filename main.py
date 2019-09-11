''' Executes all scripts '''
import os
import time
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Executes all scripts. ''', epilog="""Main""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


from parsers._configparser import getConfigs


def get_args(key):
    return str(parse_arguments().__dict__[key])


if __name__ == "__main__":
    start_time_main = time.time()

    config_file = get_args("config")

    if getConfigs("Operations", "querying", config_file) == "True":
        os.system("python3 " + "startStaging.py")

    if getConfigs("Operations", "Retrieve", config_file) == "True":
        start_data_retrive_time = time.time()
        os.system("python3 " + "downloadDataproducts.py")
        end_data_retrive_time = time.time()
        print("Data selection time", end_data_retrive_time  - start_data_retrive_time)

    if getConfigs("Operations", "Process", config_file) == "True":
        start_data_process_time = time.time()
        os.system("python3 " + "runPipelins.py")
        end_data_process_time = time.time()
        print("Data download time", end_data_process_time - start_data_process_time)

    end_time_main = time.time()
    print("Total time ", end_time_main - start_time_main)
