from awlofar.main.aweimports import *

from parsers._configparser import getConfigs


class Querying:
    uris = dict()
    invalid_files = dict()
    valid_files = dict()

    def __init__(self, SASids, calibrator, config_file):
        self.SASids = SASids
        self.calibrator = calibrator
        self.config_file = config_file
        self.targetName = getConfigs("Data", "TargetName", self.config_file)
        self.observations = {s: "" for s in self.SASids}
        self.cls = CorrelatedDataProduct

        for SASid in self.SASids:
            query_observations = (getattr(Process, "observationId") == SASid) & (Process.isValid > 0)

            if len(query_observations) > 0:
                for observation in query_observations:
                    self.observations[SASid] = observation

    def get_station_count(self):
        station_count = {}

        for SASid in self.SASids:
            observation = self.observations[SASid]
            station_count[SASid] = {"Core stations": observation.nrStationsCore,
                                    "Remote stations": observation.nrStationsRemote,
                                    "International stations": observation.nrStationsInternational,
                                    "Total stations": observation.numberOfStations}

        return(station_count)

    def get_station_count_message(self):
        message = ""
        for SASid in self.SASids:
            observation = self.observations[SASid]
            message += "For SAS id " + str(SASid) + \
                       " Core stations " + str(observation.nrStationsCore) + \
                       " Remote stations " + str(observation.nrStationsRemote) + \
                       " International stations " + str(observation.nrStationsInternational) + \
                       " Total stations " + str(observation.numberOfStations) + "\n"
        return message

    def __get_data_products(self):

        for SASid in self.SASids:
            Querying.invalid_files[SASid] = 0
            Querying.valid_files[SASid] = 0
            Querying.uris[SASid] = set()
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
                            Querying.uris[SASid].add(fileobject.URI)
                            print(fileobject.URI)
                            Querying.valid_files[SASid] += 1

                    elif getConfigs("Data", "ProductType", self.config_file) == "pipeline":

                        if '/L' + str(SASid) in fileobject.URI and "dppp" in fileobject.URI:
                            Querying.uris[SASid].add(fileobject.URI)
                            Querying.valid_files[SASid] += 1

                    else:
                        print("Wrong data product type requested")
                else:
                    Querying.invalid_files[SASid] += 1

            data_product_query = self.cls.observations.contains(observation)
            data_product_query &= self.cls.isValid == 0

            for _ in data_product_query:
                Querying.invalid_files[SASid] += 1

    def get_valid_file(self):
        return Querying.valid_files

    def get_invalid_file(self):
        return Querying.invalid_files

    def get_valid_file_message(self):
        if len(Querying.invalid_files) == 0 and len(Querying.valid_files) == 0:
            self.__get_data_products()

        message = ""
        for SASid in self.SASids:
            message += "For SAS id " + str(SASid) + \
                       " valid files is " + str(Querying.valid_files[SASid]) + \
                       " invalid files are " + str(Querying.invalid_files[SASid]) + "\n"
        return message

    def get_SURI(self):

        if len(self.uris) == 0:
            self.__get_data_products()

        return Querying.uris

