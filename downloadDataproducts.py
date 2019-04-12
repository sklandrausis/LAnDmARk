import time
import os
from stager_access import *
from parsers._configparser import ConfigParser

def getConfigs(key, value):
    configFilePath = "config.cfg"
    config = ConfigParser.getInstance()
    config.CreateConfig(configFilePath)
    return config.getConfig(key, value)

if __name__ == "__main__":
    tmpStagesIDs = set([])
    while True:
        progess = get_progress()
        if progess != None:
            stagesIDs = list(progess.keys())
            for id in stagesIDs:
                tmpStagesIDs.add(id)
            print("status IDs", stagesIDs)

            for stageID in stagesIDs:
                status = progess[stageID]["Status"]
                print("status ID", stageID)
                print("status", status)
                print("Files done", progess[stageID]["Files done"])
                print("User id", progess[stageID]["User id"])
                print("Flagged abort", progess[stageID]["Flagged abort"])
                print("File count", progess[stageID]["File count"])
                print("Percent done", progess[stageID]["Percent done"])
                print("Location", progess[stageID]["Location"], "\n")

        else:
            for id in tmpStagesIDs:
                surl = get_surls_online(int(id))
                download(surl, getConfigs("Paths", "WorkingPath") + "targets")

            break

        time.sleep(30)

    print("done")
