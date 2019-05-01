import os
import coloredlogs, logging
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *
import matplotlib.pyplot as plt
import numpy as np

from parsers._configparser import getConfigs

coloredlogs.install(level='PRODUCTION', filename='tmp.log', filemode='w')
logger = logging.getLogger('startStaging')
logging.getLogger()

class Staging(object):
    __slots__=("SASids", "targetName", "SURIs", "dataGoodnes", "logText", "calibrator", "calibratorsList")
    def __init__(self, SASids, calibrator):
        self.SASids = SASids
        self.targetName = getConfigs("Data", "TargetName", "config.cfg")
        self.SURIs = dict()
        self.dataGoodnes = dict()
        self.logText = ""
        self.calibrator = calibrator
        self.calibratorsList = list()

    def getSURI(self, SASid):
        uris = set()
        self.dataGoodnes[str(SASid)] = dict()
        logging.info("SAS id " + str(SASid))

        self.logText += "SAS id " + str(SASid) + "\n"
        if self.calibrator == False:
            self.logText += "Target name " +  self.targetName + "\n"
            logging.info("Target name " + self.targetName)

        cls = CorrelatedDataProduct
        queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

        if len(queryObservations) > 0:
            for observation in queryObservations:

                logging.info("Querying ObservationID " + observation.observationId)
                self.logText += "Querying ObservationID " + str(observation.observationId) + "\n"

                logging.info("Core stations " + str(observation.nrStationsCore) + " Remote stations " + str(observation.nrStationsRemote) + " International stations " + str(observation.nrStationsInternational) + " Total stations " + str(observation.numberOfStations))
                self.logText += "Core stations " + str(observation.nrStationsCore) + " Remote stations " + str(observation.nrStationsRemote) + " International stations " + str(observation.nrStationsInternational) + " Total stations " + str(observation.numberOfStations) + "\n"
                self.dataGoodnes[str(SASid)]["Core_stations"] = observation.nrStationsCore
                self.dataGoodnes[str(SASid)]["Remote_station"] = observation.nrStationsRemote
                self.dataGoodnes[str(SASid)]["International_stations"] = observation.nrStationsInternational

                dataproduct_query = cls.observations.contains(observation)
                if self.calibrator == False:
                    dataproduct_query &= cls.subArrayPointing.targetName == self.targetName

                else:
                    self.calibratorsList.append(observation.observationDescription.split("/")[1])
                    logging.info("Calibrator source " + observation.observationDescription.split("/")[1])
                    self.logText += "Calibrator source " + observation.observationDescription.split("/")[1]

                validFiles = 0
                invalidFiles = 0

                for dataproduct in dataproduct_query:
                    fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')

                    if fileobject:
                        if '/L' + str(SASid) in fileobject.URI:
                            uris.add(fileobject.URI)
                            validFiles += 1
                            print("File nr :", validFiles, "URI found", fileobject.URI)
                            self.logText += "File nr : " + str(validFiles) + " URI found " + str(fileobject.URI) + "\n"
                    else:
                        invalidFiles += 1
                        print("No URI found for %s with dataProductIdentifier", (dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))
                        self.logText += "No URI found for %s with dataProductIdentifier " +  str((dataproduct.__class__.__name__, dataproduct.dataProductIdentifier)) + "\n"

            logging.info("Total URI's found " + str(len(uris)))
            logging.info("Valid files found " + str(validFiles) +  " Invalid files found " + str(invalidFiles))
            self.logText += "Total URI's found " + str(len(uris)) + "\n"
            self.logText += "Valid files found " + str(validFiles) + " Invalid files found " + str(invalidFiles) + "\n"
            self.dataGoodnes[str(SASid)]["validFiles"] = validFiles
            self.dataGoodnes[str(SASid)]["invalidFiles"] = invalidFiles

        else:
            logging.error("Wrong SAS id " + SASid)
            self.logText += "Wrong SAS id " + SASid + "\n"

        self.SURIs[str(SASid)] = uris
        return uris

    def getAllCalibrators(self):
        return self.calibratorsList

    def startStaging(self):
        for id in  self.SASids:
            stager = LtaStager()
            stager.stage_uris(self.SURIs[str(id)])

    def query(self):
        for id in self.SASids:
            self.getSURI(id)

    def plot(self):
        ratios = []
        cStations = []
        rStations = []
        iStations = []
        for id in self.SASids:
            ratios.append(self.dataGoodnes[str(id)]["validFiles"] / (self.dataGoodnes[str(id)]["validFiles"] + self.dataGoodnes[str(id)]["invalidFiles"]))
            cStations.append(self.dataGoodnes[str(id)]["Core_stations"])
            rStations.append(self.dataGoodnes[str(id)]["Remote_station"])
            iStations.append(self.dataGoodnes[str(id)]["International_stations"])

        width = 0.35
        ind = np.arange(0, len(self.SASids))

        fig, ax = plt.subplots()
        p1 = ax.bar(ind, cStations, width, color='r')
        p2 = ax.bar(ind + width, rStations, width, color='g')
        p3 = ax.bar(ind + width, iStations, width, color='b')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels((self.SASids))
        ax.legend((p1[0], p2[0], p3[0]), ('Core stations', 'Remote stations', 'International stations'))
        ax.autoscale_view()
        plt.xlabel("SAS id")
        plt.grid()
        plt.show()

        plt.figure("Percent of valid data")
        plt.bar(self.SASids, np.array(ratios) * 100)
        plt.xticks(self.SASids, self.SASids)
        plt.xlabel("SAS id")
        plt.ylabel("Percent")
        plt.grid()
        plt.show()

    def getLogs(self):
        return self.logText

    def writeLogs(self, logText):
        f = ""
        for file in os.listdir('.'):
            if ".log" in file:
                log = open(file, "a+")
                f = file
                break

        log.write(logText)
        os.system("mv " + f + " " + getConfigs("Paths", "WorkingPath", "config.cfg") + "/logs/"  + f)

if __name__ == "__main__":
    SASidsTarget = [int(id) for id in getConfigs("Data", "SASids", "config.cfg").replace(" ", "").split(",")]
    SASidsCalibrator = [id - 1 for id in SASidsTarget]

    logging.info("Processing target")
    stagingTarget = Staging(SASidsTarget, False)
    stagingTarget.query()
    stagingTarget.plot()
    tmpTargetLogs = stagingTarget.getLogs()
    logsTMP = "Processing target\n" + tmpTargetLogs

    logging.info("Processing calibrators")
    stagingCalibrator = Staging(SASidsCalibrator, True)
    stagingCalibrator.query()
    stagingCalibrator.plot()
    tmpCalibratorLogs = stagingCalibrator.getLogs()
    logsTMP = logsTMP + "\nProcessing calibrators\n" + tmpCalibratorLogs
    os.system("python3.6 " + "setup.py " + str(stagingCalibrator.getAllCalibrators()).replace(",", " ").replace("[", "").replace("]", ""))
    stagingCalibrator.writeLogs(logsTMP)

    if getConfigs("Operations", "Stage", "config.cfg") == "True":
        stagingTarget.startStaging()
        stagingCalibrator.startStaging()
