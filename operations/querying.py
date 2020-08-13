#!/usr/bin/env python3
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from services.querying_service import query
from parsers._configparser import getConfigs

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
working_dir = getConfigs("Paths", "WorkingPath", config_file)
target_name = getConfigs("Data", "TargetName", config_file)
working_dir = working_dir + "/" + target_name + "/"
aux_dir = working_dir + "/LAnDmARk_aux"


def plot_querying_results(q1, q2):
    width = 0.35
    ind = np.arange(0, len(sas_ids_target))
    fig = plt.figure("Number of stations", figsize=(50, 50))

    def plot_station_count_calibrator():
        axc = fig.add_subplot(1, 2, 2)
        station_count_q1 = q1.get_station_count()
        cStationsCalibrator = []
        rStationsCalibrator = []
        iStationsCalibrator = []
        tStationsCalibrator = []

        for id in sas_ids_calibrator:
            cStationsCalibrator.append(station_count_q1[id]["Core stations"])
            rStationsCalibrator.append(station_count_q1[id]["Remote stations"])
            iStationsCalibrator.append(station_count_q1[id]["International stations"])
            tStationsCalibrator.append(station_count_q1[id]["Total stations"])

        pc1 = axc.bar(ind, cStationsCalibrator, width, color='r', bottom=[0, 0])
        pc2 = axc.bar(ind, rStationsCalibrator, width, color='g', bottom=cStationsCalibrator)
        bottom_tmp = [cStationsCalibrator[b] + rStationsCalibrator[b] for b in
                      range(0, len(cStationsCalibrator))]
        pc3 = axc.bar(ind, iStationsCalibrator, width, color='b', bottom=bottom_tmp)
        axc.set_xticks(ind)
        axc.set_xticklabels(sas_ids_calibrator)
        axc.legend((pc1[0], pc2[0], pc3[0]), ('Core stations', 'Remote stations', 'International stations'))
        axc.autoscale_view()
        axc.set_title("Calibrator")
        axc.set_xlabel("SAS id")
        plt.grid()

    def plot_station_count_target():
        axt = fig.add_subplot(1, 2, 1)
        station_count_q2 = q2.get_station_count()
        cStationsTarget = []
        rStationsTarget = []
        iStationsTarget = []
        tStationsTarget = []

        for id in sas_ids_target:
            cStationsTarget.append(station_count_q2[id]["Core stations"])
            rStationsTarget.append(station_count_q2[id]["Remote stations"])
            iStationsTarget.append(station_count_q2[id]["International stations"])
            tStationsTarget.append(station_count_q2[id]["Total stations"])

        pt1 = axt.bar(ind, cStationsTarget, width, color='r', bottom=[0, 0])
        pt2 = axt.bar(ind, rStationsTarget, width, color='g', bottom=cStationsTarget)
        bottom_tmp = [cStationsTarget[b] + rStationsTarget[b] for b in range(0, len(cStationsTarget))]
        pt3 = axt.bar(ind, iStationsTarget, width, color='b', bottom=bottom_tmp)
        axt.set_xticks(ind)
        axt.set_xticklabels(sas_ids_target)
        axt.legend((pt1[0], pt2[0], pt3[0]), ('Core stations', 'Remote stations', 'International stations'))
        axt.autoscale_view()
        axt.set_title("Target")
        axt.set_xlabel("SAS id")
        plt.grid()

    if getConfigs("Operations", "which_obj", config_file) == "calibrators":
        plot_station_count_calibrator()

    elif getConfigs("Operations", "which_obj", config_file) == "targets":
        plot_station_count_target()

    elif getConfigs("Operations", "which_obj", config_file) == "all":
        plot_station_count_calibrator()
        plot_station_count_target()

    plt.savefig(aux_dir + "/selection/" + "station_count_per_sas_id.png")

    plt.figure("Percent of valid data", figsize=(25, 25))

    def plot_valid_files_calibrator():
        valid_files = q1.get_valid_file()
        invalid_files = q1.get_invalid_file()
        ratiosCalibrator = []
        for id in sas_ids_calibrator:
            ratiosCalibrator.append(valid_files[id] / (valid_files[id] + invalid_files[id]))

        plt.subplot(1, 2, 2)
        plt.bar(sas_ids_calibrator, np.array(ratiosCalibrator) * 100, color='g')
        plt.xticks(sas_ids_calibrator, sas_ids_calibrator)
        plt.xlabel("SAS id")
        plt.ylabel("Percent")
        plt.title("Calibrator")
        plt.grid()

    def plot_valid_files_target():
        valid_files = q2.get_valid_file()
        invalid_files = q2.get_invalid_file()
        ratiosTarget = []
        for id in sas_ids_target:
            ratiosTarget.append(valid_files[id] / (valid_files[id] + invalid_files[id]))

        plt.subplot(1, 2, 1)
        plt.bar(sas_ids_target, np.array(ratiosTarget) * 100, color='g')
        plt.xticks(sas_ids_target, sas_ids_target)
        plt.xlabel("SAS id")
        plt.ylabel("Percent")
        plt.title("Target")
        plt.grid()

    if getConfigs("Operations", "which_obj", config_file) == "calibrators":
        plot_valid_files_calibrator()

    elif getConfigs("Operations", "which_obj", config_file) == "targets":
        plot_valid_files_target()

    elif getConfigs("Operations", "which_obj", config_file) == "all":
        plot_valid_files_calibrator()
        plot_valid_files_target()

    plt.savefig(aux_dir + "/selection/" + "valid_data_per_sas_id.png")


def main():
    if not os.path.exists("querying_results.txt"):
        os.system("touch querying_results.txt")
    querying_results = open("querying_results.txt", "w")
    suri_file_name_calibrator = "calibrator"
    suri_file_name_target = "target"
    suri_file_name_calibrators = []
    suri_file_name_targets = []

    for sas_ids in sas_ids_calibrator:
        suri_file_name_calibrator = "calibrator"
        suri_file_name_calibrator += "_" + str(sas_ids)
        if getConfigs("Data", "subbandselect", config_file) == "True":
            suri_file_name_calibrator += "_" + \
                                         getConfigs("Data", "minsubband", config_file) + "_" + \
                                         getConfigs("Data", "maxsubband", config_file)
        if getConfigs("Operations", "which_obj", config_file) == "calibrators":
            os.system("touch " + suri_file_name_calibrator)
            suri_file_name_calibrators.append(suri_file_name_calibrator)

    for sas_ids in sas_ids_target:
        suri_file_name_target = "target"
        suri_file_name_target += "_" + str(sas_ids)
        if getConfigs("Data", "subbandselect", config_file) == "True":
            suri_file_name_target += "_" + \
                                         getConfigs("Data", "minsubband", config_file) + "_" + \
                                         getConfigs("Data", "maxsubband", config_file)
        if getConfigs("Operations", "which_obj", config_file) == "targets":
            os.system("touch " + suri_file_name_target)
            suri_file_name_targets.append(suri_file_name_target)

    if getConfigs("Operations", "which_obj", config_file) == "all":
        for sas_ids in sas_ids_calibrator:
            suri_file_name_calibrator = "calibrator"
            suri_file_name_calibrator += "_" + str(sas_ids)
            if getConfigs("Data", "subbandselect", config_file) == "True":
                suri_file_name_calibrator += "_" + \
                                             getConfigs("Data", "minsubband", config_file) + "_" + \
                                             getConfigs("Data", "maxsubband", config_file)

            os.system("touch " + suri_file_name_calibrator)
            suri_file_name_calibrators.append(suri_file_name_calibrator)

        for sas_ids in sas_ids_target:
            suri_file_name_target = "target"
            suri_file_name_target += "_" + str(sas_ids)
            if getConfigs("Data", "subbandselect", config_file) == "True":
                suri_file_name_target += "_" + \
                                         getConfigs("Data", "minsubband", config_file) + "_" + \
                                         getConfigs("Data", "maxsubband", config_file)

            os.system("touch " + suri_file_name_target)
            suri_file_name_targets.append(suri_file_name_target)
    q1, q2 = query(sas_ids_calibrator, sas_ids_target, config_file)

    if q1 is None:
        msg_st = q2.get_station_count_message()
        querying_results.write(msg_st)
        querying_results.write("\n")
        msg_d = q2.get_valid_file_message()
        querying_results.write(msg_d)
        querying_results.write("\n")
        suri = q2.get_SURI()
        index = 0
        for sas_ids in sas_ids_target:
            with open(suri_file_name_targets[index], "w") as suri_file:
                for si in suri[sas_ids]:
                    suri_file.write(si)
                    suri_file.write("\n")
            index += 1
    elif q2 is None:
        msg_st = q1.get_station_count_message()
        querying_results.write(msg_st)
        querying_results.write("\n")
        msg_d = q1.get_valid_file_message()
        querying_results.write(msg_d)
        querying_results.write("\n")
        suri = q1.get_SURI()
        index = 0
        for sas_ids in sas_ids_calibrator:
            with open(suri_file_name_calibrators[index], "w") as suri_file:
                for si in suri[sas_ids]:
                    suri_file.write(si)
                    suri_file.write("\n")
            index +=1
    else:
        msg1_st = q1.get_station_count_message()
        msg2_st = q2.get_station_count_message()
        msg_st = msg1_st + "\n" + msg2_st
        querying_results.write(msg_st)
        querying_results.write("\n")
        msg1_d = q1.get_valid_file_message()
        msg2_d = q2.get_valid_file_message()
        msg_d = msg1_d + "\n" + msg2_d
        querying_results.write(msg_d)
        querying_results.write("\n")
        suri = q2.get_SURI()
        indexc = 0
        for sas_id in sas_ids_target:
            with open(suri_file_name_targets[indexc], "w") as suri_file:
                for si in suri[sas_id]:
                    suri_file.write(si)
                    suri_file.write("\n")
            indexc += 1

        suri = q1.get_SURI()
        indext = 0
        for sas_id in sas_ids_calibrator:
            with open(suri_file_name_calibrators[indext], "w") as suri_file:
                for si in suri[sas_id]:
                    suri_file.write(si)
                    suri_file.write("\n")
            indext += 1

    querying_results.write("done")
    querying_results.close()
    plot_querying_results(q1, q2)
    sys.exit(0)


if __name__ == "__main__":
    main()
