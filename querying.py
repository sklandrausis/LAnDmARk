from awlofar.main.aweimports import *

from parsers._configparser import getConfigs


class Querying:

    def __init__(self, SASids, calibrator, config_file):
        self.SASids = SASids
        self.calibrator = calibrator
        self.config_file = config_file
        self.targetName = getConfigs("Data", "TargetName", self.config_file)
        self.observations = {s: "" for s in self.SASids}
        self.cls = CorrelatedDataProduct
        self.uris = set()

        for SASid in self.SASids:
            query_observations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

            if len(query_observations) > 0:
                for observation in query_observations:
                    self.observations[SASid] = observation

    def get_station_count(self):
        message = ""
        for SASid in self.SASids:
            observation = self.observations[SASid]
            message += "For SAS id " + str(SASid) + \
                       " Core stations " + str(observation.nrStationsCore) + \
                       " Remote stations " + str(observation.nrStationsRemote) + \
                       " International stations " + str(observation.nrStationsInternational) + \
                       " Total stations " + str(observation.numberOfStations) + "\n"
        return message

    def get_data_products(self):
        message = ""

        for SASid in self.SASids:
            invalid_files = 0
            valid_files = 0
            observation = self.observations[SASid]
            data_product_query = self.cls.observations.contains(observation)
            data_product_query &= self.cls.isValid == 1

            if not self.calibrator:
                data_product_query &= self.cls.subArrayPointing.targetName == self.targetName

            for data_product in data_product_query:
                fileobject = ((FileObject.data_object == data_product) & (FileObject.isValid > 0)).max('creation_date')
                if fileobject:
                    if getConfigs("Data", "ProductType", self.config_file) == "observation":
                        if '/L' + str(SASid) in fileobject.URI and not "dppp" in fileobject.URI:
                            self.uris.add(fileobject.URI)
                            valid_files += 1
                            print("File nr :", valid_files, "URI found", fileobject.URI)

                    elif getConfigs("Data", "ProductType", self.config_file) == "pipeline":

                        if '/L' + str(SASid) in fileobject.URI and "dppp" in fileobject.URI:
                            self.uris.add(fileobject.URI)
                            valid_files += 1

                    else:
                        print("Wrong data product type requested")
                else:
                    invalid_files += 1

            data_product_query = self.cls.observations.contains(observation)
            data_product_query &= self.cls.isValid == 0

            for _ in data_product_query:
                invalid_files += 1

            message += "For SAS id " + str(SASid) + \
                       " valid files is " + str(valid_files) + \
                       " invalid files are " + str(invalid_files) + "\n"

        return message
