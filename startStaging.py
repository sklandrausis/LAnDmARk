import os
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *
import matplotlib.pyplot as plt
import numpy as np

from parsers._configparser import ConfigParser

def getConfigs(key, value):
    configFilePath = "config.cfg"
    config = ConfigParser.getInstance()
    config.CreateConfig(configFilePath)
    return config.getConfig(key, value)

class Staging(object):
    __slots__=("SASids", "targetName", "SURIs", "dataGoodnes")
    def __init__(self, SASids):
        self.SASids = SASids
        self.targetName = getConfigs("Data", "TargetName")
        self.SURIs = dict()
        self.dataGoodnes = dict()

    def getSURI(self, SASid):
        uris = set()

        print("SAS id", SASid)
        print("Target name", self.targetName)
        cls = CorrelatedDataProduct
        queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

        if len(queryObservations) > 0:

            for observation in queryObservations:
                print("Querying ObservationID", observation.observationId)
                dataproduct_query = cls.observations.contains(observation)
                dataproduct_query &= cls.subArrayPointing.targetName == self.targetName

                # print(len(dataproduct_query))

                validFiles = 0
                invalidFiles = 0
                for dataproduct in dataproduct_query:
                    fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max(
                        'creation_date')

                    if fileobject:
                        if '/L' + str(SASid) in fileobject.URI:
                            uris.add(fileobject.URI)
                            validFiles += 1
                            print("File nr :", validFiles, "URI found", fileobject.URI)
                    else:
                        invalidFiles += 1
                        print("No URI found for %s with dataProductIdentifier", (dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))

            print("Total URI's found %d" % len(uris))
            print("Valid files found ", validFiles, " Invalid files found ", invalidFiles, "\n")
            self.dataGoodnes[str(SASid)] = {"validFiles":validFiles, "invalidFiles":invalidFiles}

            os.system("rm " + "*.log")

        else:
            print("Wrong SAS id ", SASid, "\n")

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
        plt.bar(SASids, ratios)
        plt.xticks(SASids, SASids)
        plt.xlabel("SAS id")
        plt.ylabel("ratios")
        plt.show()

if __name__ == "__main__":
    SASids = [int(id) for id in getConfigs("Data", "SASids").replace(" ", "").split(",")]
    staging = Staging(SASids)
    staging.query()
    staging.plot()

    if getConfigs("Data", "Stage") == "True":
        staging.startStaging()

