#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import threading
import time
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import numpy as np
from services.stager_access import get_progress
from services.querying_service import Querying
from parsers._configparser import getConfigs

sns.set()
rcParams["font.size"] = 18
rcParams["legend.fontsize"] = "xx-large"
rcParams["ytick.major.size"] = 14
rcParams["xtick.major.size"] = 14
rcParams["axes.labelsize"] = 18


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Run selected operations. ''')
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


config_file = get_args("config")

SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")]
project = getConfigs("Data", "PROJECTid", config_file)

if len(getConfigs("Data", "calibratorSASids", config_file)) == 0:
    if project == "MSSS_HBA_2013":
        SASidsCalibrator = [id - 1 for id in SASidsTarget]

    else:
        raise Exception("SAS id for calibrator is not set in config.cfg file")
else:
    SASidsCalibrator = [int(id) for id in
                        getConfigs("Data", "calibratorSASids", config_file).replace(" ", "").split(",")]

workingDir = getConfigs("Paths", "WorkingPath", config_file)
targetName = getConfigs("Data", "TargetName", config_file)
workingDir = workingDir + "/" + targetName + "/"
auxDir = workingDir + "/LAnDmARk_aux"


def query():
    if getConfigs("Operations", "which_obj", config_file) == "calibrators":
        q1 = Querying(SASidsCalibrator, True, config_file)
        q2 = None
    elif getConfigs("Operations", "which_obj", config_file) == "targets":
        q1 = None
        q2 = Querying(SASidsTarget, False, config_file)
    else:
        q1 = Querying(SASidsCalibrator, True, config_file)
        q2 = Querying(SASidsTarget, False, config_file)
    return q1, q2


def plot_querying_results(q1, q2):
    width = 0.35
    ind = np.arange(0, len(SASidsTarget))
    fig = plt.figure("Number of stations", figsize=(50, 50))

    def plot_station_count_calibrator():
        axc = fig.add_subplot(1, 2, 2)
        station_count_q1 = q1.get_station_count()
        cStationsCalibrator = []
        rStationsCalibrator = []
        iStationsCalibrator = []
        tStationsCalibrator = []

        for id in SASidsCalibrator:
            cStationsCalibrator.append(station_count_q1[id]["Core stations"])
            rStationsCalibrator.append(station_count_q1[id]["Remote stations"])
            iStationsCalibrator.append(station_count_q1[id]["International stations"])
            tStationsCalibrator.append(station_count_q1[id]["Total stations"])

        # pc4 = axc.bar(ind - width, tStationsCalibrator, width/2, color='y')
        pc1 = axc.bar(ind, cStationsCalibrator, width, color='r', bottom=[0, 0])
        pc2 = axc.bar(ind, rStationsCalibrator, width, color='g', bottom=cStationsCalibrator)
        bottom_tmp = [cStationsCalibrator[b] + rStationsCalibrator[b] for b in
                      range(0, len(cStationsCalibrator))]
        pc3 = axc.bar(ind, iStationsCalibrator, width, color='b', bottom=bottom_tmp)
        axc.set_xticks(ind)
        axc.set_xticklabels((SASidsCalibrator))
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

        for id in SASidsTarget:
            cStationsTarget.append(station_count_q2[id]["Core stations"])
            rStationsTarget.append(station_count_q2[id]["Remote stations"])
            iStationsTarget.append(station_count_q2[id]["International stations"])
            tStationsTarget.append(station_count_q2[id]["Total stations"])

        # pt4 = axt.bar(ind - width, tStationsTarget, width/2, color='y')
        pt1 = axt.bar(ind, cStationsTarget, width, color='r', bottom=[0, 0])
        pt2 = axt.bar(ind, rStationsTarget, width, color='g', bottom=cStationsTarget)
        bottom_tmp = [cStationsTarget[b] + rStationsTarget[b] for b in range(0, len(cStationsTarget))]
        pt3 = axt.bar(ind, iStationsTarget, width, color='b', bottom=bottom_tmp)
        axt.set_xticks(ind)
        axt.set_xticklabels((SASidsTarget))
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

    plt.savefig(auxDir + "/selection/" + "station_count_per_sas_id.png")

    plt.figure("Percent of valid data", figsize=(25, 25))

    def plot_valid_files_calibrator():
        valid_files = q1.get_valid_file()
        invalid_files = q1.get_invalid_file()
        ratiosCalibrator = []
        for id in SASidsCalibrator:
            ratiosCalibrator.append(valid_files[id] / (valid_files[id] + invalid_files[id]))

        plt.subplot(1, 2, 2)
        plt.bar(SASidsCalibrator, np.array(ratiosCalibrator) * 100, color='g')
        plt.xticks(SASidsCalibrator, SASidsCalibrator)
        plt.xlabel("SAS id")
        plt.ylabel("Percent")
        plt.title("Calibrator")
        plt.grid()

    def plot_valid_files_target():
        valid_files = q2.get_valid_file()
        invalid_files = q2.get_invalid_file()
        ratiosTarget = []
        for id in SASidsTarget:
            ratiosTarget.append(valid_files[id] / (valid_files[id] + invalid_files[id]))

        plt.subplot(1, 2, 1)
        plt.bar(SASidsTarget, np.array(ratiosTarget) * 100, color='g')
        plt.xticks(SASidsTarget, SASidsTarget)
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

    plt.savefig(auxDir + "/selection/" + "valid_data_per_sas_id.png")


def main():
    q1, q2 = query()

    if getConfigs("Operations", "querying", config_file) == "True":
        querying_results = open("querying_results.txt", "w")

        if q1 is None:
            msg_st = q2.get_station_count_message()
            querying_results.write(msg_st)
            querying_results.write("\n")
            msg_d = q2.get_valid_file_message()
            querying_results.write(msg_d)
            querying_results.write("\n")
        elif q2 is None:
            msg_st = q1.get_station_count_message()
            querying_results.write(msg_st)
            querying_results.write("\n")
            msg_d = q1.get_valid_file_message()
            querying_results.write(msg_d)
            querying_results.write("\n")
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

        querying_results.write("done")
        querying_results.close()

        plot_querying_results(q1, q2)

    if getConfigs("Operations", "stage", config_file) == "True":

        if q1 is not None:
            if len(q1.valid_files) == 0:
                calibrator_SURI = q1.get_SURI()
            else:
                calibrator_SURI = q1.uris
        else:
            calibrator_SURI = ""

        if q2 is not None:
            if len(q2.valid_files) == 0:
                target_SURI = q2.get_SURI()
            else:
                target_SURI = q2.uris
        else:
            target_SURI = ""

        if calibrator_SURI is not "":
            sas_ids_string = ""
            suris_string = ""
            for sas_id in range(0, len(SASidsCalibrator)):
                for uri in range(0, len(calibrator_SURI[SASidsCalibrator[sas_id]])):
                    if uri == len(SASidsCalibrator) - 1:
                        suris_string += list(calibrator_SURI[SASidsCalibrator[sas_id]])[uri] + "#"
                    else:
                        suris_string += list(calibrator_SURI[SASidsCalibrator[sas_id]])[uri] + "#"

                if sas_id == len(SASidsCalibrator) - 1:
                    sas_ids_string += str(SASidsCalibrator[sas_id])
                else:
                    sas_ids_string += str(SASidsCalibrator[sas_id]) + "_"

            t = threading.Thread(target=subprocess.Popen, args=(["nohup", "./stage.py", sas_ids_string, suris_string],))
            t.start()
            t.join()
            while True:
                progress = get_progress()
                if progress is None:
                    break
                time.sleep(30)

        if target_SURI is not "":
            sas_ids_string = ""
            suris_string = ""
            for sas_id in range(0, len(SASidsTarget)):
                for uri in range(0, len(target_SURI[SASidsTarget[sas_id]])):
                    if uri == len(SASidsCalibrator) - 1:
                        suris_string += list(target_SURI[SASidsTarget[sas_id]])[uri] + "#"
                    else:
                        suris_string += list(target_SURI[SASidsTarget[sas_id]])[uri] + "#"

                if sas_id == len(SASidsTarget) - 1:
                    sas_ids_string += str(SASidsTarget[sas_id])
                else:
                    sas_ids_string += str(SASidsTarget[sas_id]) + "_"
                    suris_string += "&"

            t = threading.Thread(target=subprocess.Popen,
                                 args=(["nohup", "./stage.py", sas_ids_string, suris_string],))
            t.start()
            t.join()
            while True:
                progress = get_progress()
                if progress is None:
                    break
                time.sleep(30)

    if getConfigs("Operations", "retrieve", config_file) == "True":
        sas_ids_string_calibrator = ""
        sas_ids_string_target = ""
        suffix_urls_string = ""
        download_dir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                       getConfigs("Data", "TargetName", "config.cfg") + "/"

        for sas_id in range(0, len(SASidsCalibrator)):
            if sas_id == len(SASidsCalibrator) - 1:
                sas_ids_string_calibrator += str(SASidsCalibrator[sas_id])
            else:
                sas_ids_string_calibrator += str(SASidsCalibrator[sas_id]) + "_"

        for sas_id in range(0, len(SASidsTarget)):
            if sas_id == len(SASidsTarget) - 1:
                sas_ids_string_target += str(SASidsTarget[sas_id])
            else:
                sas_ids_string_target += str(SASidsTarget[sas_id]) + "_"

        if q1 is not None:
            if len(q1.valid_files) == 0:
                calibrator_SURI = q1.get_SURI()
            else:
                calibrator_SURI = q1.uris
        else:
            calibrator_SURI = ""

        if q2 is not None:
            if len(q2.valid_files) == 0:
                target_SURI = q2.get_SURI()
            else:
                target_SURI = q2.uris
        else:
            target_SURI = ""

        suffix_urls = []
        if calibrator_SURI != "":
            for sas_id in SASidsCalibrator:
                suffix_urls.extend(calibrator_SURI[sas_id])

        if target_SURI != "":
            for sas_id in SASidsTarget:
                suffix_urls.extend(target_SURI[sas_id])

        for s in range(0, len(suffix_urls)):
            if s == len(suffix_urls) - 1:
                suffix_urls_string += suffix_urls[s]
            else:
                suffix_urls_string += suffix_urls[s] + "#"

        t = threading.Thread(target=subprocess.Popen, args=(["nohup", "./retrieve.py", '"' + suffix_urls_string + '"',
                                                             download_dir, sas_ids_string_calibrator,
                                                             sas_ids_string_target],))
        t.start()
        t.join()

        retrieve_files_percent = dict()
        if getConfigs("Operations", "which_obj", config_file) == "calibrators":
            for sas_id in SASidsCalibrator:
                retrieve_files_percent[sas_id] = []

        elif getConfigs("Operations", "which_obj", config_file) == "targets":
            for sas_id in SASidsTarget:
                retrieve_files_percent[sas_id] = []
        else:
            for sas_id in SASidsCalibrator:
                retrieve_files_percent[sas_id] = []
            for sas_id in SASidsTarget:
                retrieve_files_percent[sas_id] = []

        for sas_id in retrieve_files_percent:
            retrieve_files_percent[sas_id].append(0)

        while True:
            percent_done = []

            for sas_id_ in list(retrieve_files_percent.keys()):
                if sas_id_ in SASidsCalibrator:
                    directory = download_dir + "calibrators/" + str(sas_id_) + "_RAW/"
                elif sas_id_ in SASidsTarget:
                    directory = download_dir + "targets/" + str(sas_id_) + "_RAW/"

                if directory != "":
                    with open("querying_results.txt", "r") as querying_results:
                        lines = querying_results.readlines()
                        for line in lines:
                            if str(sas_id_) in line and "valid files" in line:
                                valid_files = int(line.split(" ")[7])
                                break

                file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
                                  and ".tar" in f or ".MS" in f])

                percent_done.append(file_count / valid_files)

            if sum(percent_done) == len(percent_done):
                break

    if getConfigs("Operations", "process", config_file) == "True":
        threading.Thread(target=subprocess.Popen, args=(["./run_pipelines.py"],)).start()

    sys.exit(0)


if __name__ == "__main__":
    main()