import time

from parsers._configparser import getConfigs
from stager_access import *

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
                SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", "config.cfg").replace(" ", "").split(",")]

                project = getConfigs("Data", "PROJECTid", "config.cfg")
                if len(getConfigs("Data", "calibratorSASids", "config.cfg")) == 0:
                    if project == "MSSS_HBA_2013":
                        SASidsCalibrator = [id - 1 for id in SASidsTarget]

                    else:
                        raise Exception("SAS id for calibrator is not set in config.cfg file")
                        sys.exit(1)
                else:
                    SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", "config.cfg").replace(" ", "").split(",")]

                download(surl, getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/", SASidsCalibrator, SASidsTarget) # Download calibrator

            break

        time.sleep(30)

    print("done")
