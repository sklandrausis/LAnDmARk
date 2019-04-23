import os
import coloredlogs, logging
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *
import matplotlib.pyplot as plt

from parsers._configparser import getConfigs

coloredlogs.install(level='PRODUCTION', filename='tmp.log', filemode='w')
logger = logging.getLogger('startStaging')
logging.getLogger()

class Staging(object):
    __slots__=("SASids", "targetName", "SURIs", "dataGoodnes", "logText", "calibrator")
    def __init__(self, SASids, calibrator):
        self.SASids = SASids
        self.targetName = getConfigs("Data", "TargetName", "config.cfg")
        self.SURIs = dict()
        self.dataGoodnes = dict()
        self.logText = ""
        self.calibrator = calibrator

    def getSURI(self, SASid):
        uris = set()
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

                dataproduct_query = cls.observations.contains(observation)
                if self.calibrator == False:
                    dataproduct_query &= cls.subArrayPointing.targetName == self.targetName
                else:
                    print("cls.subArrayPointing.targetName", cls.subArrayPointing.targetName)

                #print(len(dataproduct_query))

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
            self.dataGoodnes[str(SASid)] = {"validFiles":validFiles, "invalidFiles":invalidFiles}

            #os.system("rm " + "*.log")

        else:
            logging.error("Wrong SAS id " + SASid)
            self.logText += "Wrong SAS id " + SASid + "\n"

        self.SURIs[str(SASid)] = uris
        return uris

    def startStaging(self):
        for id in  self.SASids:
            stager = LtaStager()
            stager.stage_uris(self.SURIs[str(id)])

    def query(self):
        for id in self.SASids:
            self.getSURI(id)

    def plot(self):
        ratios = []
        for id in self.SASids:
            ratios.append (self.dataGoodnes[str(id)]["validFiles"] /  (self.dataGoodnes[str(id)]["validFiles"] +  self.dataGoodnes[str(id)]["invalidFiles"]))

        plt.figure("Ratio of valid data")
        plt.bar(self.SASids, ratios)
        plt.xticks(self.SASids, self.SASids)
        plt.xlabel("SAS id")
        plt.ylabel("ratios")
        plt.show()

    def writeLogs(self):
        f = ""
        for file in os.listdir('.'):
            if ".log" in file:
                log = open(file, "a+")
                f = file
                break

        log.write(self.logText)
        #os.system("mv " + f + " " + getConfigs("Paths", "WorkingPath", "config.cfg") + "/logs/"  + f)


#only one log file is created!!!

if __name__ == "__main__":
    SASidsTarget = [int(id) for id in getConfigs("Data", "SASids", "config.cfg").replace(" ", "").split(",")]
    SASidsCalibrator = [id - 1 for id in SASidsTarget]

    print("Processing target")
    stagingTarget = Staging(SASidsTarget, False)
    stagingTarget.query()
    stagingTarget.plot()
    stagingTarget.writeLogs()

    print("Processing calibrators")
    stagingCalibrator = Staging(SASidsCalibrator, True)
    stagingCalibrator.query()
    stagingCalibrator.plot()
    stagingCalibrator.writeLogs()

    if getConfigs("Operations", "Stage", "config.cfg") == "True":
        stagingTarget.startStaging()
        stagingCalibrator.startStaging()
