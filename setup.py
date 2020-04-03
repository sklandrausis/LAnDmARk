import os
import sys
import argparse

from parsers._configparser import setConfigs, getConfigs


def create_directory(dir_name):
    os.system("mkdir -p " + dir_name)


def copy_files(file_from, file_to):
    os.system("cp -rfu " + file_from + "  " + file_to)


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Setup working directory tree. ''', epilog="""Setup""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


if __name__ == "__main__":
    config_file = get_args("config")
    workingDir = getConfigs("Paths", "WorkingPath", config_file)
    targetName = getConfigs("Data", "TargetName",config_file)
    workingDir = workingDir + "/" + targetName + "/"
    PrefactorDir = getConfigs("Paths", "PrefactorPath", config_file) + "/"
    targetSASids = getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")
    project = getConfigs("Data", "PROJECTid", config_file)
    task_file = getConfigs("Paths", "task_file", config_file)

    if len(getConfigs("Data", "calibratorSASids", config_file)) == 0:
        if project == "MSSS_HBA_2013":
            SASidsCalibrator = [int(id) - 1 for id in targetSASids]

        else:
            raise Exception("SAS id for calibrator is not set in config.cfg file")
            sys.exit(1)
    else:
        SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", config_file).replace(" ", "").split(",")]

    imagingDir = workingDir + "imaging_deep" + "/"
    calibratorDir = workingDir + "calibrators" + "/"
    targetDir = workingDir + "targets" + "/"
    auxDir = workingDir + "/LAnDmARk_aux"
    calibratorDirResults = workingDir + "calibrators/" + "calibrators_results" + "/"
    targetDirResults = workingDir + "targets/" + "targets_results" + "/"
    lofarroot = getConfigs("Paths", "lofarroot", config_file)
    casaroot = getConfigs("Paths", "casaroot", config_file)
    pyraproot = getConfigs("Paths", "pyraproot", config_file)
    hdf5root = getConfigs("Paths", "hdf5root", config_file)
    wcsroot = getConfigs("Paths", "wcsroot", config_file)
    losotopath = getConfigs("Paths", "losotoPath", config_file)
    aoflagger = getConfigs("Paths", "aoflagger", config_file)
    max_per_node = getConfigs("Cluster", "max_per_node", config_file)
    method = getConfigs("Cluster", "method", config_file)
    wsclean_executable = getConfigs("Paths", "wsclean_executable", config_file)
    pythonpath = getConfigs("Paths", "pythonpath", config_file)

    # Creating directory structure
    create_directory(workingDir)
    create_directory(auxDir)
    create_directory(auxDir + "/selection")
    create_directory(auxDir + "/stage")
    create_directory(auxDir + "/retrieve")

    def setup_calibrator():
        for id in SASidsCalibrator:
            print("Setup for calibrator id", id)
            id = str(id)
            create_directory(calibratorDir + id + "_RAW")
            job_directory = workingDir + "calibrators/calibrators_results/"
            log_file = workingDir + "calibrators/" + "pipeline_" + id + ".log"

            # Creating calibrator files
            copy_files(PrefactorDir + 'pipeline.cfg', calibratorDir + id + "_RAW/")
            copy_files(PrefactorDir + 'Pre-Facet-Calibrator.parset', calibratorDir + id + "_RAW/")
            setConfigs("DEFAULT", "lofarroot", lofarroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "casaroot", casaroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "pyraproot", pyraproot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "hdf5root", hdf5root, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "wcsroot", wcsroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "runtime_directory", calibratorDir + id + "_RAW",
                       calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "working_directory", calibratorDir + id + "_RAW",
                       calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "pythonpath", pythonpath, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("remote", "max_per_node", max_per_node, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("layout", "job_directory", job_directory, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "task_files", task_file, calibratorDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("logging", "log_file", log_file, calibratorDir + id + "_RAW" + "/pipeline.cfg")

            with open(calibratorDir + id + "_RAW" + '/Pre-Facet-Calibrator.parset', "r") as parset_file:
                parset_file = parset_file.readlines()

            for line in parset_file:
                if "! cal_input_path" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! cal_input_path          =  " + calibratorDir + id + "_RAW" + "  ## specify the directory where your calibrator data is stored\n")

                elif "! cal_input_pattern" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! cal_input_pattern       =  " + "L" + "*.MS" + "  ## regular expression pattern of all your calibrator files\n")

                elif "! prefactor_directory" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! prefactor_directory      =  " + PrefactorDir + "  ## path to your prefactor copy\n")

                elif "! losoto_directory" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! losoto_directory       =   " + losotopath + "  ## path to your local LoSoTo installation\n")

                elif "! aoflagger" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! aoflagger       =   " + aoflagger + "  ## path to your aoflagger executable\n")

                elif "! job_directory " in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! job_directory        =   " + job_directory + "  ## directory of the prefactor outputs\n")

                elif "! results_directory " in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! results_directory        =   " + "{{ job_directory }}/results" + "  ## location of the results\n")

                elif "! inspection_directory " in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! inspection_directory         =   " + "{{ results_directory }}/inspection_" + id + "  ## directory where the inspection plots will be stored \n")

                elif "! cal_values_directory " in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! cal_values_directory        =   " + "{{ results_directory }}/cal_values_" + id + "  ## directory where the final h5parm solution set will be stored \n")

            with open(calibratorDir + id + "_RAW" + '/Pre-Facet-Calibrator.parset', "w") as parset_filew:
                parset_filew.write("".join(parset_file))

    def setup_target():
        for id in targetSASids:
            print("Setup for target id", id)
            create_directory(targetDir + id + "_RAW")

            # Creating target files
            copy_files(PrefactorDir + 'pipeline.cfg', targetDir + id + "_RAW")
            copy_files(PrefactorDir + 'Pre-Facet-Target.parset', targetDir + id + "_RAW")
            setConfigs("DEFAULT", "lofarroot", lofarroot, targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "casaroot", casaroot, targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "pyraproot", pyraproot, targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "hdf5root", hdf5root, targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "wcsroot", wcsroot, targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "runtime_directory", targetDir + id + "_RAW",
                       targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "working_directory", targetDir + id + "_RAW",
                       targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("DEFAULT", "pythonpath", pythonpath, targetDir + id + "_RAW" + "/pipeline.cfg")
            setConfigs("remote", "max_per_node", max_per_node, targetDir + id + "_RAW" + "/pipeline.cfg")

            with open(targetDir + id + "_RAW" + "/Pre-Facet-Target.parset", "r") as parset_file:
                parset_file = parset_file.readlines()

            for line in parset_file:
                if "! target_input_path" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! target_input_path          =  " + targetDir + id + "_RAW" + "  ## specify the directory where your target data is stored\n")

                elif "! target_input_pattern" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! target_input_pattern       =  " + "L" + "*.MS" + "  ## regular expression pattern of all your calibrator files\n")

                elif "! prefactor_directory" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! prefactor_directory      =  " + PrefactorDir + "  ## path to your prefactor copy\n")

                elif "! losoto_directory" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! losoto_directory       =   " + losotopath + "  ## path to your local LoSoTo installation\n")

                elif "! aoflagger" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! aoflagger       =   " + aoflagger + "  ## path to your aoflagger executable\n")

                elif "! cal_solutions" in line:
                    parset_file[parset_file.index(line)] = line.replace(line,
                                                                        "! cal_solutions             =  " + calibratorDir + str(
                                                                            SASidsCalibrator[targetSASids.index(
                                                                                id)]) + "_RAW/Pre-Facet-Calibrator/results/cal_values/cal_solutions.h5" + "\n")

            with open(targetDir + id + "_RAW" + "/Pre-Facet-Target.parset", "w") as parset_filew:
                for line in parset_file:
                    parset_filew.write(line)

    if getConfigs("Operations", "which_obj", config_file) == "calibrators":
        create_directory(calibratorDir)
        create_directory(calibratorDirResults)
        setup_calibrator()

    elif getConfigs("Operations", "which_obj", config_file) == "target":
        create_directory(targetDir)
        create_directory(targetDirResults)
        setup_target()

    elif getConfigs("Operations", "which_obj", config_file) == "all":
        create_directory(calibratorDir)
        create_directory(calibratorDirResults)
        create_directory(targetDir)
        create_directory(targetDirResults)
        create_directory(imagingDir)
        setup_calibrator()
        setup_target()

        copy_files(PrefactorDir + 'pipeline.cfg', imagingDir)
        copy_files(PrefactorDir + 'Pre-Facet-Image.parset', imagingDir)
        setConfigs("DEFAULT", "lofarroot", lofarroot, imagingDir + "pipeline.cfg")
        setConfigs("DEFAULT", "casaroot", casaroot, imagingDir + "pipeline.cfg")
        setConfigs("DEFAULT", "pyraproot", pyraproot, imagingDir + "pipeline.cfg")
        setConfigs("DEFAULT", "hdf5root", hdf5root, imagingDir + "pipeline.cfg")
        setConfigs("DEFAULT", "wcsroot", wcsroot, imagingDir + "pipeline.cfg")
        setConfigs("DEFAULT", "runtime_directory", imagingDir, imagingDir + "pipeline.cfg")
        setConfigs("DEFAULT", "working_directory", workingDir, imagingDir + "pipeline.cfg")
        setConfigs("DEFAULT", "pythonpath", pythonpath, imagingDir + "pipeline.cfg")
        setConfigs("remote", "max_per_node", max_per_node, imagingDir + "pipeline.cfg")

        with open(imagingDir + "/Pre-Facet-Image.parset", "r") as parset_file:
            parset_file = parset_file.readlines()

        for line in parset_file:
            if "! data_input_path" in line:
                parset_file[parset_file.index(line)] = line.replace(line,
                                                                    "! data_input_path          =  " + targetDirResults + "  ## specify the directory where your concatenated target data are stored\n")

            elif "! data_input_pattern" in line:
                parset_file[parset_file.index(line)] = line.replace(line,
                                                                    "! data_input_pattern       =  L*.pre-cal.ms    ## regular expression pattern of all your calibrator files\n")

            elif "! prefactor_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line,
                                                                    "! prefactor_directory      =  " + PrefactorDir + "  ## path to your prefactor copy\n")

            elif "wsclean_executable" in line:
                parset_file[parset_file.index(line)] = line.replace(line,
                                                                    "! wsclean_executable       =   " + wsclean_executable + "  ## path to your local WSClean executable\n")

        with open(imagingDir + "/Pre-Facet-Image.parset"
                               "", "w") as parset_filew:
            parset_filew.write("".join(parset_file))

    sys.exit(0)
