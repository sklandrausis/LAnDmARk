#!/usr/bin/env python3
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parsers._configparser import getConfigs
from services.querying_service import query
from services.stager_access import download


def main():
    config_file = "config.cfg"
    sas_ids_target = [int(id) for id in getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")]
    project = getConfigs("Data", "PROJECTid", config_file)

    if len(getConfigs("Data", "calibratorSASids", config_file)) == 0:
        if project == "MSSS_HBA_2013":
            sas_ids_calibrator = [id - 1 for id in sas_ids_target]

        else:
            raise Exception("SAS id for calibrator is not set in config.cfg file")
    else:
        sas_ids_calibrator = [int(id) for id in
                              getConfigs("Data", "calibratorSASids",
                                         config_file).replace(" ", "").split(",")]

    download_dir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                   getConfigs("Data", "TargetName", "config.cfg") + "/"

    suri_file_name_calibrators = []
    suri_file_name_targets = []

    for sas_ids in sas_ids_calibrator:
        suri_file_name_calibrator = "calibrator"
        suri_file_name_calibrator += "_" + str(sas_ids)
        if getConfigs("Data", "subbandselect", config_file) == "True":
            suri_file_name_calibrator += "_" + \
                                         getConfigs("Data", "minsubband", config_file) + "_" + \
                                         getConfigs("Data", "maxsubband", config_file)

        if getConfigs("Data", "frequencyselect", config_file) == "True":
            suri_file_name_calibrator += "_" + \
                                         getConfigs("Data", "minfrequency", config_file) + "_" + \
                                         getConfigs("Data", "maxfrequency", config_file)

        if os.path.isfile(suri_file_name_calibrator) and \
                getConfigs("Operations", "which_obj", config_file) == "calibrators":
            suri_file_name_calibrators.append(suri_file_name_calibrator)

    for sas_ids in sas_ids_target:
        suri_file_name_target = "target"
        suri_file_name_target += "_" + str(sas_ids)
        if getConfigs("Data", "subbandselect", config_file) == "True":
            suri_file_name_target += "_" + \
                                     getConfigs("Data", "minsubband", config_file) + "_" + \
                                     getConfigs("Data", "maxsubband", config_file)

        if getConfigs("Data", "frequencyselect", config_file) == "True":
            suri_file_name_target += "_" + \
                                     getConfigs("Data", "minfrequency", config_file) + "_" + \
                                     getConfigs("Data", "maxfrequency", config_file)

        if os.path.isfile(suri_file_name_target) and \
                getConfigs("Operations", "which_obj", config_file) == "targets":
            suri_file_name_targets.append(suri_file_name_target)

    if getConfigs("Operations", "which_obj", config_file) == "all":
        for sas_ids in sas_ids_calibrator:
            suri_file_name_calibrator = "calibrator"
            suri_file_name_calibrator += "_" + str(sas_ids)
            if getConfigs("Data", "subbandselect", config_file) == "True":
                suri_file_name_calibrator += "_" + \
                                             getConfigs("Data", "minsubband", config_file) + "_" + \
                                             getConfigs("Data", "maxsubband", config_file)

            if getConfigs("Data", "frequencyselect", config_file) == "True":
                suri_file_name_calibrator += "_" + \
                                             getConfigs("Data", "minfrequency", config_file) + "_" + \
                                             getConfigs("Data", "maxfrequency", config_file)

            if os.path.isfile(suri_file_name_calibrator):
                suri_file_name_calibrators.append(suri_file_name_calibrator)

        for sas_ids in sas_ids_target:
            suri_file_name_target = "target"
            suri_file_name_target += "_" + str(sas_ids)
            if getConfigs("Data", "subbandselect", config_file) == "True":
                suri_file_name_target += "_" + \
                                         getConfigs("Data", "minsubband", config_file) + "_" + \
                                         getConfigs("Data", "maxsubband", config_file)

            if getConfigs("Data", "frequencyselect", config_file) == "True":
                suri_file_name_target += "_" + \
                                         getConfigs("Data", "minfrequency", config_file) + "_" + \
                                         getConfigs("Data", "maxfrequency", config_file)

            if os.path.isfile(suri_file_name_target):
                suri_file_name_targets.append(suri_file_name_target)

    target_suri = ""
    calibrator_suri = ""

    def get_target_suri():
        target_suri_tmp = ""
        if len(suri_file_name_targets) > 0:
            for si in range(0, len(suri_file_name_targets)):
                suri = open(suri_file_name_targets[si], "r").readlines()[
                       0:len(open(suri_file_name_targets[si], "r").readlines())]
                target_suri_tmp = {sas_ids_target[si]: suri}

        else:
            if len(q2.valid_files) == 0:
                target_suri_tmp = q2.get_SURI()
            else:
                target_suri_tmp = q2.uris
        return target_suri_tmp

    def get_calibrator_suri():
        calibrator_suri_tmp = ""
        if len(suri_file_name_calibrators) > 0:
            for si in range(0, len(suri_file_name_calibrators)):
                suri = open(suri_file_name_calibrators[si], "r").readlines()[0:
                                                                             len(open(suri_file_name_calibrators[si],
                                                                                      "r").readlines())]
                calibrator_suri_tmp = {sas_ids_calibrator[si]: suri}
        else:
            if len(q1.valid_files) == 0:
                calibrator_suri_tmp = q1.get_SURI()
            else:
                calibrator_suri_tmp = q1.uris
        return calibrator_suri_tmp

    q1, q2 = query(sas_ids_calibrator, sas_ids_target, config_file)

    if q1 is None:
        target_suri = get_target_suri()

    if q2 is None:
        calibrator_suri = get_calibrator_suri()

    if q1 is not None and q2 is not None:
        target_suri = get_target_suri()
        calibrator_suri = get_calibrator_suri()

    suffix_urls = []
    if calibrator_suri != "":
        for sas_id in sas_ids_calibrator:
            suffix_urls.extend(calibrator_suri[sas_id])

    if target_suri != "":
        for sas_id in sas_ids_target:
            suffix_urls.extend(target_suri[sas_id])

    for suffix_url in suffix_urls:
        download([suffix_url], download_dir, sas_ids_calibrator, sas_ids_target)
    sys.exit(0)


if __name__ == "__main__":
    main()