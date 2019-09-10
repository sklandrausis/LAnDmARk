''' Executes all scripts '''
import os
import time

from parsers._configparser import getConfigs

if __name__ == "__main__":
    start_time_main = time.time()

    if getConfigs("Operations", "querying", "config.cfg") == "True":
        os.system("python3 " + "startStaging.py")

    if getConfigs("Operations", "Retrieve", "config.cfg") == "True":
        start_data_retrive_time = time.time()
        os.system("python3 " + "downloadDataproducts.py")
        end_data_retrive_time = time.time()
        print("Data selection time", end_data_retrive_time  - start_data_retrive_time)

    if getConfigs("Operations", "Process", "config.cfg") == "True":
        start_data_process_time = time.time()
        os.system("python3 " + "runPipelins.py")
        end_data_process_time = time.time()
        print("Data download time", end_data_process_time - start_data_process_time)

    end_time_main = time.time()
    print("Total time ", end_time_main - start_time_main)
