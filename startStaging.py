import os
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from awlofar.main.aweimports import *

from parsers._configparser import ConfigParser

def getConfigs(key, value):
    configFilePath = "config.cfg"
    config = ConfigParser.getInstance()
    config.CreateConfig(configFilePath)
    return config.getConfig(key, value)

if __name__ == "__main__":
    do_stage = False
    uris = set()
    SASid = int(getConfigs("Data", "SASid"))
    print("SAS id", SASid)
    targetName = getConfigs("Data", "TargetName")
    print("Target name", targetName)
    cls = CorrelatedDataProduct
    queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

    for observation in queryObservations:
        print("Querying ObservationID",  observation.observationId)
        dataproduct_query = cls.observations.contains(observation)
        dataproduct_query &= cls.subArrayPointing.targetName == targetName

        #print(len(dataproduct_query))

        count_files = 0
        for dataproduct in dataproduct_query:
            fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')

            if fileobject:
                if '/L' + str(SASid) in fileobject.URI:
                    uris.add(fileobject.URI)
                    count_files = count_files + 1
                    print("File nr :", count_files, "URI found", fileobject.URI)
            else:
                print("No URI found for %s with dataProductIdentifier", (dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))

    print("Total URI's found %d" % len(uris))

    os.system("rm " + "*.log")

    if do_stage:
        stager = LtaStager()
        stager.stage_uris(uris)