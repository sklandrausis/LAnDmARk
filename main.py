''' Executes all scripts '''
import os
import sys
import time
import argparse
from imp import find_module
from sys import version_info

from parsers._configparser import getConfigs


def checkPythonmod(mod):
	"""
	Verify if a package is (not) installed.
	Args:
	mod: python package name
	Returns: print statement if (not) found.
	Raises:
	TypeError : If input package not installed.
	"""
	nomod = 0
	try:
		op = find_module(mod)
		#print(' Module %s installed' % mod)
	except ImportError:
		nomod = nomod+1
		print(' Module %s NOT found: please install it!' % mod)
	return nomod

print(' Loading modules...')
pkgs = ['coloredlogs', 'awlofar', 'matplotlib', 'numpy', 'seaborn']
nrnomod = 0
for package in pkgs:
    nrnomod = nrnomod + checkPythonmod(package)

if nrnomod != 0:
	raise TypeError(' ERROR: Not all dependencies found.')

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
    python_version = version_info.major

    start_time_main = time.time()

    config_file = get_args("config")
    python_version = getConfigs("Paths", "pythonversion", config_file)

    if python_version == 3:

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

    elif python_version == 2:
        if getConfigs("Operations", "querying", config_file) == "True":
            if get_args("print_logs") == "True":
                os.system("python2 " + "selectionStaging.py -d")
            else:
                os.system("python2 " + "selectionStaging.py")

        if getConfigs("Operations", "Retrieve", config_file) == "True":
            start_data_retrive_time = time.time()
            os.system("python2 " + "retrieveDataproducts.py")
            end_data_retrive_time = time.time()
            print("Data selection time", end_data_retrive_time  - start_data_retrive_time)

        if getConfigs("Operations", "Process", config_file) == "True":
            start_data_process_time = time.time()
            os.system("python2 " + "runPipelines.py")
            end_data_process_time = time.time()
            print("Data download time", end_data_process_time - start_data_process_time)

    else:
        print("Python version is not suported !")

    end_time_main = time.time()
    print("Total time ", end_time_main - start_time_main)
