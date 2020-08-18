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
                threads.append(tc)

            for id in sas_ids_target:
                parset_target = target_dir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
                config_target = target_dir + str(id) + "_RAW/" + "pipeline.cfg"
                tt = threading.Thread(target=run_pipeline, args=(parset_target, config_target,))
                threads.append(tt)

            parset_image = image_dir + "Pre-Facet-Image.parset"
            config_image = image_dir + "pipeline.cfg"
            ti = threading.Thread(target=run_pipeline, args=(parset_image, config_image,))
            threads.append(ti)

        elif getConfigs("Operations", "which_obj", "config.cfg") == "targets":

            for id in sas_ids_target:
                parset_target = target_dir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
                config_target = target_dir + str(id) + "_RAW/" + "pipeline.cfg"
                tt = threading.Thread(target=run_pipeline, args=(parset_target, config_target,))
                threads.append(tt)
        else:
            for id in sas_ids_calibrator:
                parset_calib = calibrator_dir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
                config_calib = calibrator_dir + str(id) + "_RAW/" + "pipeline.cfg"
                tc = threading.Thread(target=run_pipeline, args=(parset_calib, config_calib,))
                threads.append(tc)

        for thread in threads:
            thread.start()
            thread.join()

    @property
    def name(self):
        return self.__name
