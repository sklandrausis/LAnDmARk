import os
import sys
import time
import coloredlogs, logging
from awlofar.database.Context import context
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import numpy as np
import argparse
import warnings

from parsers._configparser import getConfigs


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Executes all scripts. ''', epilog="""Main""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-d", "--print_logs", help="Print log", action="store_true", default=False)
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


coloredlogs.install(level='PRODUCTION', filename='tmp.log', filemode='w')
logger = logging.getLogger('startStaging')
logging.getLogger()

sns.set()

rcParams["font.size"] = 18
rcParams["legend.fontsize"] = "xx-large"
rcParams["ytick.major.size"] = 14
rcParams["xtick.major.size"] = 14
rcParams["axes.labelsize"] = 18

class Staging():
    
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
        logging.info("SAS id " + str(SASid))
        config_file = get_args("config")

        self.logText += "SAS id " + str(SASid) + "\n"
        if self.calibrator == False:
            self.logText += "Target name " +  self.targetName + "\n"
            logging.info("Target name " + self.targetName)

        cls = CorrelatedDataProduct
        queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

        if len(queryObservations) > 0:
            validFiles = 0
            invalidFiles = 0

            for observation in queryObservations:

                logging.info("Querying ObservationID " + observation.observationId)
                self.logText += "Querying ObservationID " + str(observation.observationId) + "\n"

                if "UnspecifiedProcess" in str(type(observation)):
                    invalidFiles += 1
                    dataproduct_query = cls.observations.contains(observation)
                    dataproduct_query &= cls.isValid == 1

                    if get_args("print_logs") == "True":
                        print("Possibly corrupted file", len(dataproduct_query))
                        print("Possibly staging", observation.can_be_staged, "Number of unspecified data products", observation.numberOfUnspecifiedDataProducts)

                else:
                    logging.info("Core stations " + str(observation.nrStationsCore) + " Remote stations " + str(observation.nrStationsRemote) + " International stations " + str(observation.nrStationsInternational) + " Total stations " + str(observation.numberOfStations))
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
                    logging.info("Calibrator source " + observation.observationDescription.split("/")[1])
                    self.logText += "Calibrator source " + observation.observationDescription.split("/")[1]

                for dataproduct in dataproduct_query:
                    fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')

                    if fileobject:
                        if getConfigs("Data", "ProductType", config_file) == "observation":
                            if '/L' + str(SASid) in fileobject.URI and not "dppp" in fileobject.URI:
                                uris.add(fileobject.URI)
                                validFiles += 1
                                if get_args("print_logs") == "True":
                                    print("File nr :", validFiles, "URI found", fileobject.URI)
                                self.logText += "File nr : " + str(validFiles) + " URI found " + str(fileobject.URI) + "\n"
                                self.dataGoodnes[str(SASid)]["file_size"] = fileobject.filesize

                        elif getConfigs("Data", "ProductType", config_file) == "pipeline":

                            if '/L' + str(SASid) in fileobject.URI and "dppp" in fileobject.URI:
                                uris.add(fileobject.URI)
                                validFiles += 1
                                if get_args("print_logs") == "True":
                                    print("File nr :", validFiles, "URI found", fileobject.URI)
                                self.logText += "File nr : " + str(validFiles) + " URI found " + str(fileobject.URI) + "\n"
                                self.dataGoodnes[str(SASid)]["file_size"] = fileobject.filesize


                        else:
                            print("Wrong data product type requested")
                            exit(1)
                    else:
                        invalidFiles += 1
                        if get_args("print_logs") == "True":
                            print("No URI found for %s with dataProductIdentifier", (dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))
                        self.logText += "No URI found for %s with dataProductIdentifier " +  str((dataproduct.__class__.__name__, dataproduct.dataProductIdentifier)) + "\n"


                dataproduct_query = cls.observations.contains(observation)
                dataproduct_query &= cls.isValid == 0

                for dataproduct in dataproduct_query:
                    invalidFiles += 1

            logging.info("Total URI's found " + str(len(uris)))
            logging.info("Valid files found " + str(validFiles) + " Invalid files found " + str(invalidFiles))
            self.logText += "Total URI's found " + str(len(uris)) + "\n"
            self.logText += "Valid files found " + str(validFiles) + " Invalid files found " + str(invalidFiles) + "\n"
            self.dataGoodnes[str(SASid)]["validFiles"] = validFiles
            self.dataGoodnes[str(SASid)]["invalidFiles"] = invalidFiles

        else:
            logging.error("Wrong SAS id " + SASid)
            self.logText += "Wrong SAS id " + SASid + "\n"

        self.SURIs[str(SASid)] = uris
        return uris

    def get_total_file_size(self):
        file_size = 0
        for id in self.SASids:
            file_size += self.dataGoodnes[str(id)]["file_size"]
        return file_size

    def getSURIs(self):
        return self.SURIs

    def getAllCalibrators(self):
        return self.calibratorsList

    def getDataGoodnes(self):
        return self.dataGoodnes

    def get_total_file_count(self):
        file_count = 0
        for id in self.SASids:
            file_count += len(self.SURIs[str(id)])

        return file_count

    def startStaging(self):
        for id in  self.SASids:

            if len(self.SURIs[str(id)]) >= 5000:
                warnings.warn("file count exceeds 5000 for SAS id " + str(id), Warning)

            elif self.dataGoodnes[str(id)]["file_size"] >= 5000000000000:
                warnings.warn("file size exceeds 5 TB for SAS id " + str(id), Warning)

            else:
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
        os.system("mv " + f + " " + getConfigs("Paths", "WorkingPath", config_file) + "/" + getConfigs("Data", "TargetName", config_file) + "/LAnDmARk_aux/" + f)

def plotDataGoodnes(targetGoodnes, calibratorGoodnes, SASidsTarget, SASidsCalibrator):
    workingDir = getConfigs("Paths", "WorkingPath", config_file)
    targetName = getConfigs("Data", "TargetName", config_file)
    workingDir = workingDir + "/" + targetName + "/"
    auxDir = workingDir + "/LAnDmARk_aux"

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
    plt.bar(SASidsCalibrator, np.array(ratiosCalibrator) * 100, color='g')
    plt.xticks(SASidsCalibrator, SASidsCalibrator)
    plt.xlabel("SAS id")
    plt.ylabel("Percent")
    plt.title("Calibrator")
    plt.grid()
    
    plt.show()
    plt.savefig(auxDir + "/selection/" + "valid_data_per_sas_id.png")

    width = 0.35
    ind = np.arange(0, len(SASidsTarget))
    fig = plt.figure("Number of stations")
    axt = fig.add_subplot(1, 2, 1)
    axc = fig.add_subplot(1, 2, 2)

    #pt4 = axt.bar(ind - width, tStationsTarget, width/2, color='y')
    pt1 = axt.bar(ind, cStationsTarget, width, color='r', bottom=[0,0])
    pt2 = axt.bar(ind, rStationsTarget, width, color='g', bottom=cStationsTarget)
    bottom_tmp = [cStationsTarget[b] +  rStationsTarget[b] for b in range(0, len(cStationsTarget)) ]
    pt3 = axt.bar(ind, iStationsTarget, width, color='b', bottom=bottom_tmp)
    axt.set_xticks(ind)
    axt.set_xticklabels((SASidsTarget))
    axt.legend((pt1[0], pt2[0], pt3[0]), ('Core stations' , 'Remote stations', 'International stations'))
    axt.autoscale_view()
    axt.set_title("Target")
    axt.set_xlabel("SAS id")
    plt.grid()

    #pc4 = axc.bar(ind - width, tStationsCalibrator, width/2, color='y')
    pc1 = axc.bar(ind, cStationsCalibrator, width, color='r', bottom=[0,0])
    pc2 = axc.bar(ind, rStationsCalibrator, width, color='g', bottom=cStationsCalibrator)
    bottom_tmp = [cStationsCalibrator[b] + rStationsCalibrator[b] for b in range(0, len(cStationsCalibrator))]
    pc3 = axc.bar(ind, iStationsCalibrator, width, color='b', bottom=bottom_tmp)
    axc.set_xticks(ind)
    axc.set_xticklabels((SASidsCalibrator))
    axc.legend((pc1[0], pc2[0], pc3[0]), ('Core stations', 'Remote stations', 'International stations'))
    axc.autoscale_view()
    axc.set_title("Calibrator")
    axc.set_xlabel("SAS id")
    plt.grid()
    
    plt.show()
    plt.savefig(auxDir + "/selection/" + "station_count_per_sas_id.png")


def main():
    config_file = get_args("config")

    # Check if project is private and we are not members of project
    project = getConfigs("Data", "PROJECTid", config_file)
    context.set_project(project)

    if project != context.get_current_project().name:
        raise Exception("You are not member of project", project)
        sys.exit(1)

    SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")]

    if len(getConfigs("Data", "calibratorSASids", config_file)) == 0:
        if project == "MSSS_HBA_2013":
            SASidsCalibrator = [id - 1 for id in SASidsTarget]

        else:
            raise Exception("SAS id for calibrator is not set in config.cfg file")
            sys.exit(1)
    else:
        SASidsCalibrator = [int(id) for id in
                            getConfigs("Data", "calibratorSASids", config_file).replace(" ", "").split(",")]

    logging.info("Processing target")
    start_data_selection_time = time.time()
    stagingTarget = Staging(SASidsTarget, False, config_file)
    stagingTarget.query()
    tmpTargetLogs = stagingTarget.getLogs()
    logsTMP = "Processing target\n" + tmpTargetLogs

    logging.info("Processing calibrators")
    stagingCalibrator = Staging(SASidsCalibrator, True, config_file)
    stagingCalibrator.query()
    end_data_selection_time = time.time()
    print("Data selection time", end_data_selection_time - start_data_selection_time)
    tmpCalibratorLogs = stagingCalibrator.getLogs()

    workingDir = getConfigs("Paths", "WorkingPath", config_file)
    targetName = getConfigs("Data", "TargetName", config_file)
    workingDir = workingDir + "/" + targetName + "/"
    auxDir = workingDir + "/LAnDmARk_aux"

    targetSURIs = []
    calibratorSURIs = []

    for id in SASidsTarget:
        for URI in stagingTarget.getSURIs()[str(id)]:
            if "sara" in URI:
                targetSURIs.append("https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")
            elif "juelich" in URI:
                targetSURIs.append(
                    "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl=" + URI + "\n")
            else:
                targetSURIs.append("https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")

    for id in SASidsCalibrator:
        for URI in stagingCalibrator.getSURIs()[str(id)]:
            if "sara" in URI:
                calibratorSURIs.append(
                    "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")
            elif "juelich" in URI:
                calibratorSURIs.append(
                    "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl=" + URI + "\n")
            else:
                calibratorSURIs.append("https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")

    logsTMP = logsTMP + "\nProcessing calibrators\n" + tmpCalibratorLogs
    os.system("python3 " + "setup.py")

    for id in SASidsTarget:
        if os.path.isfile(auxDir + "/target_" + str(id) + "_SURIs" + ".txt") == False:
            with open(auxDir + "/target_" + str(id) + "_SURIs" + ".txt", "w") as targetSURIfile:
                for uri in targetSURIs:
                    if str(id) in uri:
                        targetSURIfile.write(uri)

    for id in SASidsCalibrator:
        if os.path.isfile(auxDir + "/calibrator_" + str(id) + "_SURIs" + ".txt") == False:
            with open(auxDir + "/calibrator_" + str(id) + "_SURIs" + ".txt", "w") as calibratorSURIfile:
                for uri in calibratorSURIs:
                    if str(id) in uri:
                        calibratorSURIfile.write(uri)

    stagingCalibrator.writeLogs(logsTMP)

    plotDataGoodnes(stagingTarget.getDataGoodnes(), stagingCalibrator.getDataGoodnes(), SASidsTarget, SASidsCalibrator)

    if getConfigs("Operations", "Stage", config_file) == "True":

        if stagingTarget.get_total_file_size() + stagingCalibrator.get_total_file_size() < 5000000000000 and stagingCalibrator.get_total_file_count() + stagingTarget.get_total_file_count() < 5000:
            if getConfigs("Operations", "which_obj", config_file) == "all" or len(getConfigs("Operations", "which_obj", config_file)) == 0:
                start_staging_time = time.time()
                stagingTarget.startStaging()
                stagingCalibrator.startStaging()
                end_staging_time = time.time()
                print("Staging ination time", end_staging_time - start_staging_time)

            elif getConfigs("Operations", "which_obj", config_file) == "targets":
                start_staging_time = time.time()
                stagingTarget.startStaging()
                end_staging_time = time.time()
                print("Staging ination time", end_staging_time - start_staging_time)

            elif getConfigs("Operations", "which_obj", config_file) == "calibrators":
                start_staging_time = time.time()
                stagingCalibrator.startStaging()
                end_staging_time = time.time()
                print("Staging ination time", end_staging_time - start_staging_time)

    sys.exit(0)


if __name__ == "__main__":
    main()