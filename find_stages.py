from awlofar.main.aweimports import *
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
import awlofar.main as mmm


from datetime import datetime
from awlofar.database.Context import context
from awlofar.main.aweimports import CorrelatedDataProduct, FileObject, Observation
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError

do_stage = False
project = 'LC4_010'
#RA = 277.3822
#DEC = 48.7464

#SASid = 366346

uris = {
    project: set()
}


cls = CorrelatedDataProduct
query_observations = Observation.select_all().project_only(project)

o = Observation.select_all()
print("qwerty", query_observations.copy())
print(o.add_clause("==", "observation_id", "366346"))

for observation in query_observations:
    print("Querying ObservationID %s" % observation.observationId)

    dataproduct_query = cls.observations.contains(observation)
    dataproduct_query &= cls.isValid == 1

    '''
    for process in query:
        Observation.Process = process
        query_subarr = SubArrayPointing.pointing == pointing
        for subarr in query_subarr:
            query_obs = Observation.subArrayPointings.contains(subarr)
        print(process)
    '''

    for dataproduct in dataproduct_query:
        fileobject = ((FileObject.data_object == dataproduct) & (FileObject.isValid > 0)).max('creation_date')

        if fileobject:
            print("URI found %s" % fileobject.URI)
            uris[project].add(fileobject.URI)
        else:
            print("No URI found for %s with dataProductIdentifier %d" % (
                dataproduct.__class__.__name__, dataproduct.dataProductIdentifier))

    print("Total URI's found for project %s: %d" % (project, len(uris[project])))

stager = LtaStager()
if do_stage:
    print("stage")
    stager.stage_uris(uris[project])

