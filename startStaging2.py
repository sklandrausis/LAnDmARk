import os
import sys
#import coloredlogs, logging
from awlofar.database.Context import context
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *
import matplotlib.pyplot as plt
import numpy as np

from parsers._configparser import getConfigs

#coloredlogs.install(level='PRODUCTION', filename='tmp.log', filemode='w')
#logger = logging.getLogger('startStaging')
#logging.getLogger()

class Staging(object):
    __slots__=("SASids", "targetName", "SURIs", "dataGoodnes", "logText", "calibrator", "calibratorsList", "stationCount", "configFile")
    def __init__(self, SASids, calibrator, configFile):
        self.SASids = SASids
        self.SURIs = dict()
        self.dataGoodnes = dict()
        self.logText = ""
        self.calibrator = calibrator
        self.calibratorsList = list()
        self.stationCount = dict()
        self.configFile = configFile
        self.targetName = getConfigs("Data", "TargetName", self.configFile)

    def getStationsCount(self):
        return self.stationCount

    def getSURI(self, SASid):
        uris = set()
        self.dataGoodnes[str(SASid)] = dict()
        print("SAS id " + str(SASid))

        self.logText += "SAS id " + str(SASid) + "\n"
        if self.calibrator == False:
            self.logText += "Target name " +  self.targetName + "\n"
            print("Target name " + self.targetName)

        cls = CorrelatedDataProduct
        queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

        if len(queryObservations) > 0:
            validFiles = 0
            invalidFiles = 0

            for observation in queryObservations:

                print("Querying ObservationID " + observation.observationId)
                self.logText += "Querying ObservationID " + str(observation.observationId) + "\n"

                if "UnspecifiedProcess" in str(type(observation)):
                    invalidFiles += 1
                    dataproduct_query = cls.observations.contains(observation)
                    dataproduct_query &= cls.isValid == 1

                    print("Possibly corrupted file", len(dataproduct_query))
                    print("Possibly staging", observation.can_be_staged, "Number of unspecified data products", observation.numberOfUnspecifiedDataProducts)

                else:
                    print("Core stations " + str(observation.nrStationsCore) + " Remote stations " + str(observation.nrStationsRemote) + " International stations " + str(observation.nrStationsInternational) + " Total stations " + str(observation.numberOfStations))
                    self.logText += "Core stations " + str(observation.nrStationsCore) + " Remote stations " + str(observation.nrStationsRemote) + " International stations " + str(observation.nrStationsInternational) + " Total stations " + str(observation.numberOfStations) + "\n"
                    self.dataGoodnes[str(SASid)]["Core_stations"] = observation.nrStationsCore
                    self.dataGoodnes[str(SASid)]["Remote_station"] = observation.nrStationsRemote
                    self.dataGoodnes[str(SASid)]["International_stations"] = observation.nrStationsInternational
                    self.dataGoodnes[str(SASid)]["Total_stations"] = observation.numberOfStations
                    self.stationCount = {"core":observation.nrStationsCore, "remote":observation.nrStationsRemote, "international":observation.nrStationsInternational, "total":observation.numberOfStations}

                dataproduct_query = cls.observations.contains(observation)
                dataproduct_query &= cls.isValid == 1

                if self.calibrator == False:
                    dataproduct_query &= cls.subArrayPointing.targetName == self.targetName

                else:
                    self.calibratorsList.append(observation.observationDescription.split("/")[1])
                    print("Calibrator source " + observation.observationDescription.split("/")[1])
                    self.logText += "Calibrator source " + observation.observationDescription.split("/")[1]

                for dataproduct in dataproduct_query:
                    fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')

                    if fileobject:
                        if getConfigs("Data", "ProductType", "config.cfg") == "observation":
                            if '/L' + str(SASid) in fileobject.URI and not "dppp" in fileobject.URI:
                                uris.add(fileobject.URI)
                                validFiles += 1
                                print("File nr :", validFiles, "URI found", fileobject.URI)
                                self.logText += "File nr : " + str(validFiles) + " URI found " + str(fileobject.URI) + "\n"

                        elif getConfigs("Data", "ProductType", "config.cfg") == "pipeline":

                            if '/L' + str(SASid) in fileobject.URI and "dppp" in fileobject.URI:
                                uris.add(fileobject.URI)
                                validFiles += 1
                                print("File nr :", validFiles, "URI found", fileobject.URI)
                                self.logText += "File nr : " + str(validFiles) + " URI found " + str(fileobject.URI) + "\n"

                        else:
                            print("Wrong data product type requested")
                            exit(1)
                    else:
                        invalidFiles += 1
                        print("No URI found for %s with dataProductIdentifier", (dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))
                        self.logText += "No URI found for %s with dataProductIdentifier " +  str((dataproduct.__class__.__name__, dataproduct.dataProductIdentifier)) + "\n"


                dataproduct_query = cls.observations.contains(observation)
                dataproduct_query &= cls.isValid == 0

                for dataproduct in dataproduct_query:
                    invalidFiles += 1

            print("Total URI's found " + str(len(uris)))
            print("Valid files found " + str(validFiles) + " Invalid files found " + str(invalidFiles))
            self.logText += "Total URI's found " + str(len(uris)) + "\n"
            self.logText += "Valid files found " + str(validFiles) + " Invalid files found " + str(invalidFiles) + "\n"
            self.dataGoodnes[str(SASid)]["validFiles"] = validFiles
            self.dataGoodnes[str(SASid)]["invalidFiles"] = invalidFiles

        else:
            print("Wrong SAS id " + SASid)
            self.logText += "Wrong SAS id " + SASid + "\n"

        self.SURIs[str(SASid)] = uris
        return uris

    def getSURIs(self):
        return self.SURIs

    def getAllCalibrators(self):
        return self.calibratorsList

    def getDataGoodnes(self):
        return self.dataGoodnes

    def startStaging(self):
        for id in  self.SASids:
            stager = LtaStager()
            stager.stage_uris(self.SURIs[str(id)])

    def query(self):
        for id in self.SASids:
            self.getSURI(id)

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
        os.system("mv " + f + " " + getConfigs("Paths", "WorkingPath", "config.cfg") + getConfigs("Data", "TargetName", "config.cfg") + "/Pipeline_aux/"  + f)

def plotDataGoodnes(targetGoodnes, calibratorGoodnes, SASidsTarget, SASidsCalibrator):
    ratiosTarget = []
    ratiosCalibrator = []

    cStationsTarget = []
    rStationsTarget = []
    iStationsTarget = []
    tStationsTarget = []
    cStationsCalibrator = []
    rStationsCalibrator = []
    iStationsCalibrator = []
    tStationsCalibrator = []

    for id in SASidsTarget:
        ratiosTarget.append(targetGoodnes[str(id)]["validFiles"] / (targetGoodnes[str(id)]["validFiles"] + targetGoodnes[str(id)]["invalidFiles"]))
        cStationsTarget.append(targetGoodnes[str(id)]["Core_stations"])
        rStationsTarget.append(targetGoodnes[str(id)]["Remote_station"])
        iStationsTarget.append(targetGoodnes[str(id)]["International_stations"])
        tStationsTarget.append(targetGoodnes[str(id)]["Total_stations"])

    for id in SASidsCalibrator:
        ratiosCalibrator.append(calibratorGoodnes[str(id)]["validFiles"] / (calibratorGoodnes[str(id)]["validFiles"] + calibratorGoodnes[str(id)]["invalidFiles"]))
        cStationsCalibrator.append(calibratorGoodnes[str(id)]["Core_stations"])
        rStationsCalibrator.append(calibratorGoodnes[str(id)]["Remote_station"])
        iStationsCalibrator.append(calibratorGoodnes[str(id)]["International_stations"])
        tStationsCalibrator.append(calibratorGoodnes[str(id)]["Total_stations"])

    plt.figure("Percent of valid data")

    plt.subplot(1,2,1)
    plt.bar(SASidsTarget, np.array(ratiosTarget) * 100, color='g')
    plt.xticks(SASidsTarget, SASidsTarget)
    plt.xlabel("SAS id")
    plt.ylabel("Percent")
    plt.title("Target")
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.bar(SASidsCalibrator, np.array(ratiosCalibrator) * 100, color='r')
    plt.xticks(SASidsCalibrator, SASidsCalibrator)
    plt.xlabel("SAS id")
    plt.ylabel("Percent")
    plt.title("Calibrator")
    plt.grid()

    plt.show()

    width = 0.35
    ind = np.arange(0, len(SASidsTarget))
    fig = plt.figure("Number of stations")
    axt = fig.add_subplot(1, 2, 1)
    axc = fig.add_subplot(1, 2, 2)

    #pt4 = axt.bar(ind - width, tStationsTarget, width/2, color='y')
    pt1 = axt.bar(ind, cStationsTarget, width, color='r')
    pt2 = axt.bar(ind, rStationsTarget, width, color='g')
    pt3 = axt.bar(ind, iStationsTarget, width, color='b')
    axt.set_xticks(ind)
    axt.set_xticklabels((SASidsTarget))
    axt.legend((pt1[0], pt2[0], pt3[0]), ('Core stations' , 'Remote stations', 'International stations', 'Total stations'))
    axt.autoscale_view()
    axt.set_title("Target")
    axt.set_xlabel("SAS id")
    plt.grid()

    #pc4 = axc.bar(ind - width, tStationsCalibrator, width/2, color='y')
    pc1 = axc.bar(ind, cStationsCalibrator, width, color='r')
    pc2 = axc.bar(ind, rStationsCalibrator, width, color='g')
    pc3 = axc.bar(ind, iStationsCalibrator, width, color='b')
    axc.set_xticks(ind)
    axc.set_xticklabels((SASidsCalibrator))
    axc.legend((pc1[0], pc2[0], pc3[0]), ('Core stations', 'Remote stations', 'International stations', 'Total stations'))
    axc.autoscale_view()
    axc.set_title("Calibrator")
    axc.set_xlabel("SAS id")
    plt.grid()

    plt.show()

if __name__ == "__main__":

    #Check if project is private and we are not members of project
    project = getConfigs("Data", "PROJECTid", "config.cfg")
    context.set_project(project)

    if project != context.get_current_project().name:
        raise Exception("You are not member of project", project)
        sys.exit(1)

    SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", "config.cfg").replace(" ", "").split(",")]

    if len(getConfigs("Data", "calibratorSASids", "config.cfg")) == 0:
        if project == "MSSS_HBA_2013":
            SASidsCalibrator = [id - 1 for id in SASidsTarget]

        else:
            raise Exception("SAS id for calibrator is not set in config.cfg file")
            sys.exit(1)
    else:
        SASidsCalibrator =  [int(id) for id in getConfigs("Data", "calibratorSASids", "config.cfg").replace(" ", "").split(",")]


    print("Processing target")
    stagingTarget = Staging(SASidsTarget, False, "config.cfg")
    stagingTarget.query()
    tmpTargetLogs = stagingTarget.getLogs()
    logsTMP = "Processing target\n" + tmpTargetLogs

    print("Processing calibrators")
    stagingCalibrator = Staging(SASidsCalibrator, True, "config.cfg")
    stagingCalibrator.query()
    tmpCalibratorLogs = stagingCalibrator.getLogs()

    workingDir = getConfigs("Paths", "WorkingPath", "config.cfg")
    targetName = getConfigs("Data", "TargetName", "config.cfg")
    workingDir = workingDir + "/" + targetName + "/"

    targetSURIs = ""
    calibratorSURIs = ""

    for id in SASidsTarget:
        for URI in stagingTarget.getSURIs()[str(id)]:
            if "sara" in URI:
                targetSURIs += "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n"
            elif "juelich" in URI:
                targetSURIs += "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl=" + URI + "\n"
            else:
                targetSURIs += "https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n"


    for id in SASidsCalibrator:
        for URI in stagingCalibrator.getSURIs()[str(id)]:
            if "sara" in URI:
                calibratorSURIs += "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n"
            elif "juelich" in URI:
                calibratorSURIs += "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl=" + URI + "\n"
            else:
                calibratorSURIs += "https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n"

    logsTMP = logsTMP + "\nProcessing calibrators\n" + tmpCalibratorLogs
    os.system("python3 " + "setup.py " + str(stagingCalibrator.getAllCalibrators()).replace(",", " ").replace("[", "").replace("]", ""))

    with open(workingDir + "targetSURIs.txt", "w") as targetSURIfile:
        targetSURIfile.write(targetSURIs)

    with open(workingDir + "calibratorSURIs.txt", "w") as calibratorSURIfile:
        calibratorSURIfile.write(calibratorSURIs)

    stagingCalibrator.writeLogs(logsTMP)

    plotDataGoodnes(stagingTarget.getDataGoodnes(), stagingCalibrator.getDataGoodnes(), SASidsTarget, SASidsCalibrator)

    if getConfigs("Operations", "Stage", "config.cfg") == "True":
        stagingTarget.startStaging()
        stagingCalibrator.startStaging()

    sys.exit(0)
