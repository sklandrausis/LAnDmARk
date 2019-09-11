import time

from parsers._configparser import getConfigs
from stager_access import *

from pylive import live_plotter
from progress import progress
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    tmpStagesIDs = set([])
	
    #progress is 0
    i=float(0)
	
    #plot initial values
    percent_done = []
    files_done = []

    while True:
        progess = get_progress()
        if progess != None:
            stagesIDs = list(progess.keys())
            for id in stagesIDs:
                tmpStagesIDs.add(id)
            #print("status IDs", stagesIDs)

            for stageID in stagesIDs:
                status = progess[stageID]["Status"]
                
                #old real-time plot
                #y_vec[-1] = progess[stageID]["Percent done"]
                #line1 = live_plotter(x_vec,y_vec,line1)
                #y_vec = np.append(y_vec[1:],0.0)
				
                progress(i, 100, status='Staging in progress')
                i=float(progess[stageID]["Percent done"])
                f=float(progess[stageID]["Files done"])
				
                percent_done.append(i)
                files_done.append(f)

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

                download(surl, getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/", SASidsCalibrator, SASidsTarget, )

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
