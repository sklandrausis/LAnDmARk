import os
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *

from parsers._configparser import ConfigParser

def getConfigs(key, value):
    configFilePath = "config.cfg"
    config = ConfigParser.getInstance()
    config.CreateConfig(configFilePath)
    return config.getConfig(key, value)

def startStaging(SASid):
    if getConfigs("Data", "Stage") == "True":
        do_stage = True
    else:
        do_stage = False

    uris = set()
    print("SAS id", SASid)
    targetName = getConfigs("Data", "TargetName")
    print("Target name", targetName)
    cls = CorrelatedDataProduct
    queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

    if len(queryObservations) > 0:

        for observation in queryObservations:
            print("Querying ObservationID", observation.observationId)
            dataproduct_query = cls.observations.contains(observation)
            dataproduct_query &= cls.subArrayPointing.targetName == targetName

            # print(len(dataproduct_query))

            validFiles = 0
            invalidFiles = 0
            for dataproduct in dataproduct_query:
                fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')

                if fileobject:
                    if '/L' + str(SASid) in fileobject.URI:
                        uris.add(fileobject.URI)
                        validFiles += 1
                        print("File nr :", validFiles, "URI found", fileobject.URI)
                else:
                    invalidFiles += 1
                    print("No URI found for %s with dataProductIdentifier",
                          (dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))

        print("Total URI's found %d" % len(uris))
        print("Valid files found ", validFiles, " Invalid files found ", invalidFiles, "\n")

        os.system("rm " + "*.log")

        if do_stage:
            stager = LtaStager()
            stager.stage_uris(uris)
    else:
        print("Wrong SAS id ", SASid,  "\n")


if __name__ == "__main__":
    SASids = [int(id) for id in getConfigs("Data", "SASids").replace(" ", "").split(",")]

    for id in SASids:
        startStaging(id)
