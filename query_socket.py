import sys
import re
import socket
import os
import struct

import os
import sys
import time
import coloredlogs, logging
from awlofar.database.Context import context
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *

from parsers._configparser import getConfigs


def send(text):
    host = "127.0.0.1"
    port = 9000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    text = text.encode()
    sock.sendto(text (host, 9001))
    sock.close()

class Staging():

    def __init__(self, SASids, calibrator, configFile):
        self.SASids = SASids
        self.SURIs = dict()
        self.calibrator = calibrator
        self.calibratorsList = list()
        self.stationCount = dict()
        self.configFile = configFile
        self.targetName = getConfigs("Data", "TargetName", self.configFile)

    def getSURI(self, SASid="167226"):
        uris = set()

        config_file = "config.cfg"

        if self.calibrator == False:
            self.logText += "Target name " +  self.targetName + "\n"

        cls = CorrelatedDataProduct
        queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

        if len(queryObservations) > 0:
            validFiles = 0
            invalidFiles = 0

            for observation in queryObservations:
                if "UnspecifiedProcess" in str(type(observation)):
                    invalidFiles += 1
                    dataproduct_query = cls.observations.contains(observation)
                    dataproduct_query &= cls.isValid == 1

                else:
                    print(str(observation.nrStationsCore) + " Remote stations " + str(observation.nrStationsRemote) + " International stations " + str(observation.nrStationsInternational) + " Total stations " + str(observation.numberOfStations) + "\n")
                    send("Core stations " + str(observation.nrStationsCore) + " Remote stations " + str(observation.nrStationsRemote) + " International stations " + str(observation.nrStationsInternational) + " Total stations " + str(observation.numberOfStations) + "\n")

                dataproduct_query = cls.observations.contains(observation)
                dataproduct_query &= cls.isValid == 1

                if self.calibrator == False:
                    dataproduct_query &= cls.subArrayPointing.targetName == self.targetName

                else:
                    self.calibratorsList.append(observation.observationDescription.split("/")[1])

                    self.logText += "Calibrator source " + observation.observationDescription.split("/")[1]

                for dataproduct in dataproduct_query:
                    fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')

                    if fileobject:
                        if getConfigs("Data", "ProductType", config_file) == "observation":
                            if '/L' + str(SASid) in fileobject.URI and not "dppp" in fileobject.URI:
                                uris.add(fileobject.URI)
                                validFiles += 1


                        elif getConfigs("Data", "ProductType", config_file) == "pipeline":

                            if '/L' + str(SASid) in fileobject.URI and "dppp" in fileobject.URI:
                                uris.add(fileobject.URI)
                                validFiles += 1

                        else:
                            print("Wrong data product type requested")
                            exit(1)
                    else:
                        invalidFiles += 1

                        self.logText += "No URI found for %s with dataProductIdentifier " +  str((dataproduct.__class__.__name__, dataproduct.dataProductIdentifier)) + "\n"


                dataproduct_query = cls.observations.contains(observation)
                dataproduct_query &= cls.isValid == 0

                for dataproduct in dataproduct_query:
                    invalidFiles += 1

            self.logText += "Total URI's found " + str(len(uris)) + "\n"
            self.logText += "Valid files found " + str(validFiles) + " Invalid files found " + str(invalidFiles) + "\n"

        else:
            logging.error("Wrong SAS id " + SASid)
            self.logText += "Wrong SAS id " + SASid + "\n"

        self.SURIs[str(SASid)] = uris
        return uris

