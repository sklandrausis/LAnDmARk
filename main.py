''' Executes all scripts '''
import os

from parsers._configparser import getConfigs

if __name__ == "__main__":
    os.system("python3 " + "startStaging.py")
    if getConfigs("Operations", "Retrieve", "config.cfg") == "True":
        os.system("python3 " + "downloadDataproducts.py")

    if getConfigs("Operations", "Process", "config.cfg") == "True":
        os.system("python3 " + "runPipelins.py")
