import time
import numpy as np
import matplotlib.pyplot as plt
import argparse
from stager_access import *

from parsers._configparser import getConfigs

def parse_arguments():
    parser = argparse.ArgumentParser(description='''download data products. ''', epilog="""Download""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])



if __name__ == "__main__":
    tmpStagesIDs = set([])
    config_file = get_args("config")

    #progress is 0
    i=0.0

    #plot initial values
    percent_done = []
    files_done = []

    while True:
        progess = get_progress()
        if progess != None:
            if "tuple" not in str(type(progess)):
                stagesIDs = list(progess.keys())

                for id in stagesIDs:
                    tmpStagesIDs.add(id)

                for stageID in stagesIDs:
                    status = progess[stageID]["Status"]

                    i=float(progess[stageID]["Percent done"])
                    f=float(progess[stageID]["Files done"])
                    percent_done.append(i)
                    files_done.append(f)

                    print("status ID", stageID)
                    print("status", status)
                    print("Files done", progess[stageID]["Files done"])
                    print("User id", progess[stageID]["User id"])
                    print("Flagged abort", progess[stageID]["Flagged abort"])
                    print("File count", progess[stageID]["File count"])
                    print("Percent done", progess[stageID]["Percent done"])
                    print("Location", progess[stageID]["Location"], "\n")
            else:
                print("")


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

                download(surl, getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/", SASidsCalibrator, SASidsTarget)

            break

        time.sleep(30)

    if percent_done:
        workingDir = getConfigs("Paths", "WorkingPath", config_file)
        targetName = getConfigs("Data", "TargetName", config_file)
        workingDir = workingDir + "/" + targetName + "/"
        auxDir = workingDir + "/LAnDmARk_aux"
        #create and save the plot.
        plt.style.use('ggplot')
        plt.ylabel('Percent')
        plt.xlabel('Seconds')
        plt.title('Percent done')
        y = np.array(percent_done)
        x = np.array(range(0, len(percent_done)))
        plt.plot(x,y)
        plt.twinx()
        y1 = np.array(files_done)
        plt.ylabel('Files')
        plt.plot(x,y1)
        
        plt.savefig(auxDir + "/stage/" + 'data_staged_dynamics.png')
        plt.clf()
		
	
    print("done")
