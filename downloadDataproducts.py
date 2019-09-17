import time

from parsers._configparser import getConfigs
from stager_access import *
from progress import progress
import numpy as np
import matplotlib.pyplot as plt
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Executes all scripts. ''', epilog="""Main""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


if __name__ == "__main__":
    config_file = get_args("config")
    tmpStagesIDs = set([])
    i = 0.0
    percent_done = []
    files_done = []

    while True:
        progess = get_progress()
        if progess != None:
            stagesIDs = list(progess.keys())
            for id in stagesIDs:
                tmpStagesIDs.add(id)

            for stageID in stagesIDs:
                status = progess[stageID]["Status"]
                progress(i, 100, status='Staging in progress')
                i=float(progess[stageID]["Percent done"])
                f=float(progess[stageID]["Files done"])
				
                percent_done.append(i)
                files_done.append(f)

        else:
            for id in tmpStagesIDs:
                surl = get_surls_online(int(id))
                SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")]

                project = getConfigs("Data", "PROJECTid", "config.cfg")
                if len(getConfigs("Data", "calibratorSASids", "config.cfg")) == 0:
                    if project == "MSSS_HBA_2013":
                        SASidsCalibrator = [id - 1 for id in SASidsTarget]

                    else:
                        raise Exception("SAS id for calibrator is not set in config.cfg file")
                        sys.exit(1)
                else:
                    SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", config_file).replace(" ", "").split(",")]

                download(surl, getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", config_file) + "/", SASidsCalibrator, SASidsTarget, )

            break

        time.sleep(1)

    if percent_done:
        #create and save the plot.
        plt.style.use('ggplot')
        plt.ylabel('Percent')
        plt.xlabel('Seconds')
        plt.title('Percent done')
        y = np.array(percent_done)
        x = np.array(range(0, len(percent_done)))
        plt.plot(x,y)
		
        plt.savefig('percentDone.png')
        plt.clf()
		
        
    if files_done:
        #create and save the plot.
        plt.style.use('ggplot')
        plt.ylabel('Files')
        plt.xlabel('Seconds')
        plt.title('Files done')
        y = np.array(files_done)
        x = np.array(range(0, len(files_done)))
        plt.plot(x,y)
		
        plt.savefig('filesDone.png')
        plt.clf()
	
    print("done")
