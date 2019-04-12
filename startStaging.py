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
    SASid = int(getConfigs("Project", "SASid"))
    print("SAS id", SASid)
    targetName = getConfigs("Project", "TargetName")
    print("Target name", targetName)
    cls = CorrelatedDataProduct
    queryObservations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

    for observation in queryObservations:
        print("Querying ObservationID",  observation.observationId)
        dataproduct_query = cls.observations.contains(observation)
        dataproduct_query &= cls.subArrayPointing.targetName == targetName

        for dataproduct in dataproduct_query:
            fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')
            if fileobject:
                uris.add(fileobject.URI)
                print("URI found", fileobject.URI)
            else:
                print("No URI found for %s with dataProductIdentifier", (dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))

    print("Total URI's found %d" % len(uris))

    os.system("rm " + "*.log")

    if do_stage:
        stager = LtaStager()
        stager.stage_uris(uris)