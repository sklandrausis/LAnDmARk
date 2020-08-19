import os
import threading
from operations.operation import Operation
from parsers._configparser import getConfigs


def run_pipeline(parset_file, config_file):
    try:
        os.system('genericpipeline.py ' + parset_file + ' -c ' + config_file + ' -d  -v')
    except:
        print("Something went wrong")


class Process(Operation):
    def __init__(self):
        Operation.__init__(self)
        self.__name = "process"

    def execute(self):
        threads = []
        working_dir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                      getConfigs("Data", "TargetName", "config.cfg") + "/"

        calibrator_dir = working_dir + "calibrators" + "/"
        target_dir = working_dir + "targets" + "/"
        image_dir = working_dir + "imaging_deep" + "/"

        sas_ids_target = [int(id) for id in getConfigs("Data", "targetSASids", "config.cfg").replace(" ", "").split(",")]
        project = getConfigs("Data", "PROJECTid", "config.cfg")

        if len(getConfigs("Data", "calibratorSASids", "config.cfg")) == 0:
            if project == "MSSS_HBA_2013":
                sas_ids_calibrator = [id - 1 for id in sas_ids_target]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
                sys.exit(1)
        else:
            sas_ids_calibrator = [int(id) for id in
                                getConfigs("Data", "calibratorSASids", "config.cfg").replace(" ", "").split(",")]

        if getConfigs("Operations", "which_obj", "config.cfg") == "all" or len(
                getConfigs("Operations", "which_obj", "config.cfg")) == 0:
            for id in sas_ids_calibrator:
                parset_calib = calibrator_dir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
                config_calib = calibrator_dir + str(id) + "_RAW/" + "pipeline.cfg"
                tc = threading.Thread(target=run_pipeline, args=(parset_calib, config_calib,))
                tc.setName("calibrator" + "_" + str(id))
                threads.append(tc)

            for id in sas_ids_target:
                parset_target = target_dir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
                config_target = target_dir + str(id) + "_RAW/" + "pipeline.cfg"
                tt = threading.Thread(target=run_pipeline, args=(parset_target, config_target,))
                tt.setName("target" + "_" + str(id))
                threads.append(tt)

            parset_image = image_dir + "Pre-Facet-Image.parset"
            config_image = image_dir + "pipeline.cfg"
            ti = threading.Thread(target=run_pipeline, args=(parset_image, config_image,))
            ti.setName("imaging")
            threads.append(ti)

        elif getConfigs("Operations", "which_obj", "config.cfg") == "targets":

            for id in sas_ids_target:
                parset_target = target_dir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
                config_target = target_dir + str(id) + "_RAW/" + "pipeline.cfg"
                tt = threading.Thread(target=run_pipeline, args=(parset_target, config_target,))
                tt.setName("target" + "_" + str(id))
                threads.append(tt)
        else:
            for id in sas_ids_calibrator:
                parset_calib = calibrator_dir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
                config_calib = calibrator_dir + str(id) + "_RAW/" + "pipeline.cfg"
                tc = threading.Thread(target=run_pipeline, args=(parset_calib, config_calib,))
                tc.setName("calibrator" + "_" + str(id))
                threads.append(tc)

        for thread in threads:
            if "_" in thread.getName():
                type_of_process = thread.getName().split("_")[0]
                sas_id = thread.getName().split("_")[1]
            else:
                type_of_process = "imaging"

            if type_of_process == "calibrator":
                calibrator_raw_files = [file for file in os.listdir(calibrator_dir + sas_id + "_RAW/") if ".MS" in file]
                if len(calibrator_raw_files) == 0:
                    print("For sas ir " + sas_id + " there is no calibrator raw data")
                else:
                    thread.start()
                    thread.join()

            elif type_of_process == "target":
                target_raw_files = [file for file in os.listdir(target_dir + sas_id + "_RAW/") if ".MS" in file]
                if len(target_raw_files) == 0:
                    print("For sas ir " + sas_id + " there is no target raw data")
                elif not os.path.isfile(calibrator_dir + "calibrators_results/results/cal_values_" +
                                        str(sas_ids_calibrator[sas_ids_target.index(int(sas_id))]) + "/cal_solutions.h5"):
                    print("For sas id " + sas_id + " calibration solution file do not exist")
                else:
                    thread.start()
                    thread.join()

            if type_of_process == "imaging":
                target_result_files = [file for file in os.listdir(target_dir + "targets_results/results")
                                       if "pre-cal.ms" in file]
                if len(target_result_files) == 0:
                    print("target results do not exist")
                else:
                    print("processing imaging")
                    thread.start()
                    thread.join()

    @property
    def name(self):
        return self.__name
