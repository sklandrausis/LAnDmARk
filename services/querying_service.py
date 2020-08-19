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
        self.uris = dict()
        self.invalid_files = dict()
        self.valid_files = dict()

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

        return station_count

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
            self.invalid_files[SASid] = 0
            self.valid_files[SASid] = 0
            self.uris[SASid] = set()
            observation = self.observations[SASid]
            data_product_query = self.cls.observations.contains(observation)
            if getConfigs("Data", "subbandselect", self.config_file) == "True":
                subband1 = getConfigs("Data", "minsubband", self.config_file)
                subband2 = getConfigs("Data", "maxsubband", self.config_file)
                data_product_query &= ((self.cls.subband >= subband1) & (self.cls.subband <= subband2))

            if getConfigs("Data", "frequencyselect", self.config_file) == "True":
                frequency1 = float(getConfigs("Data", "minfrequency", self.config_file))
                frequency2 = float(getConfigs("Data", "maxfrequency", self.config_file))
                data_product_query &= self.cls.minimumFrequency >= frequency1
                data_product_query &= self.cls.maximumFrequency <= frequency2
            data_product_query &= self.cls.isValid == 1

            if not self.calibrator:
                data_product_query &= self.cls.subArrayPointing.targetName == self.targetName

            for data_product in data_product_query:
                fileobject = ((FileObject.data_object == data_product) & (FileObject.isValid > 0)).max('creation_date')
                if fileobject:
                    if getConfigs("Data", "ProductType", self.config_file) == "observation":
                        if '/L' + str(SASid) in fileobject.URI and not "dppp" in fileobject.URI:
                            self.uris[SASid].add(fileobject.URI)
                            print(fileobject.URI)
                            self.valid_files[SASid] += 1

                    elif getConfigs("Data", "ProductType", self.config_file) == "pipeline":

                        if '/L' + str(SASid) in fileobject.URI and "dppp" in fileobject.URI:
                            self.uris[SASid].add(fileobject.URI)
                            self.valid_files[SASid] += 1

                    else:
                        print("Wrong data product type requested")
                else:
                    self.invalid_files[SASid] += 1

            data_product_query = self.cls.observations.contains(observation)
            data_product_query &= self.cls.isValid == 0

            for _ in data_product_query:
                self.invalid_files[SASid] += 1

    def get_valid_file(self):
        return self.valid_files

    def get_invalid_file(self):
        return self.invalid_files

    def get_valid_file_message(self):
        if len(self.invalid_files) == 0 and len(self.valid_files) == 0:
            self.__get_data_products()

        message = ""
        for SASid in self.SASids:
            message += "For SAS id " + str(SASid) + \
                       " valid files is " + str(self.valid_files[SASid]) + \
                       " invalid files are " + str(self.invalid_files[SASid]) + "\n"
        return message

    def get_SURI(self):
        if len(self.uris) == 0:
            self.__get_data_products()

        return self.uris


def query(sas_ids_calibrator, sas_ids_target, config_file):
    if getConfigs("Operations", "which_obj", config_file) == "calibrators":
        query.q1 = Querying(sas_ids_calibrator, True, config_file)
        query.q2 = None
    elif getConfigs("Operations", "which_obj", config_file) == "targets":
        query.q1 = None
        query.q2 = Querying(sas_ids_target, False, config_file)
    else:
        query.q1 = Querying(sas_ids_calibrator, True, config_file)
        query.q2 = Querying(sas_ids_target, False, config_file)
    return query.q1, query.q2
