import os
import sys
import argparse

from parsers._configparser import setConfigs, getConfigs
from parsers._parsetParser import ParsetParser


def createDirectory(DirName):
    os.system("mkdir -p " + DirName)


def copyFiles(fileFrom, fileTo):
     os.system("cp -rfu " + fileFrom + "  " + fileTo)


def parse_arguments():
    parser = argparse.ArgumentParser(description='''Setup working directory tree. ''', epilog="""Setup""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


def get_args(key):
    return str(parse_arguments().__dict__[key])


if __name__=="__main__":
    config_file = get_args("config")
    workingDir = getConfigs("Paths", "WorkingPath", config_file)
    targetName = getConfigs("Data", "TargetName",config_file)
    workingDir = workingDir + "/" + targetName + "/"
    PrefactorDir = getConfigs("Paths", "PrefactorPath", config_file) + "/"
    targetSASids = getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")
    project = getConfigs("Data", "PROJECTid", config_file)

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

    # Creating directory structure
    createDirectory(workingDir)
    createDirectory(imagingDir)
    createDirectory(calibratorDir)
    createDirectory(targetDir)
    createDirectory(auxDir)
    createDirectory(auxDir + "/selection")
    createDirectory(auxDir + "/stage")
    createDirectory(auxDir + "/retrieve")
    createDirectory(calibratorDirResults)
    createDirectory(targetDirResults)

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

    # Creating imaging files
    copyFiles(PrefactorDir + 'pipeline.cfg', imagingDir)
    copyFiles(PrefactorDir + 'Initial-Subtract.parset', imagingDir)
    setConfigs("DEFAULT", "lofarroot", lofarroot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "casaroot", casaroot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "pyraproot", pyraproot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "hdf5root", hdf5root, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "wcsroot", wcsroot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "runtime_directory", imagingDir, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "working_directory", workingDir, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "pythonpath", pythonpath, imagingDir + "pipeline.cfg")
    setConfigs("remote", "max_per_node", max_per_node, imagingDir + "pipeline.cfg")

    with open(imagingDir + "/Initial-Subtract.parset", "r") as parset_file:
        parset_file = parset_file.readlines()

    for line in parset_file:
        if "! data_input_path" in line:
            parset_file[parset_file.index(line)] = line.replace(line, "! data_input_path          =  " + targetDirResults + "  ## specify the directory where your concatenated target data are stored\n")

        elif "! data_input_pattern" in line:
            parset_file[parset_file.index(line)] = line.replace(line, "! data_input_pattern       =  L*.pre-cal.ms    ## regular expression pattern of all your calibrator files\n")

        elif "! prefactor_directory" in line:
            parset_file[parset_file.index(line)] = line.replace(line, "! prefactor_directory      =  " + PrefactorDir + "  ## path to your prefactor copy\n")

        elif "wsclean_executable" in line:
            parset_file[parset_file.index(line)] = line.replace(line, "! wsclean_executable       =   " + wsclean_executable +  "  ## path to your local WSClean executable\n")

        elif "! job_directory" in line:
            parset_file[parset_file.index(line)] = line.replace(line, "! job_directory            =  " + imagingDir + "  ## directory of the prefactor outputs\n")

    with open(imagingDir + "/Initial-Subtract.parset", "w") as parset_filew:
        parset_filew.write("".join(parset_file))

    for id in SASidsCalibrator:
        print ("Setup for calibrator id", id)
        id = str(id)
        createDirectory(calibratorDir + id + "_RAW")
        

        # Creating calibrator files
        copyFiles(PrefactorDir + 'pipeline.cfg', calibratorDir + id + "_RAW/")
        copyFiles(PrefactorDir + 'Pre-Facet-Calibrator.parset',  calibratorDir + id + "_RAW/")
        setConfigs("DEFAULT", "lofarroot", lofarroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "casaroot", casaroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "pyraproot", pyraproot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "hdf5root", hdf5root, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "wcsroot", wcsroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "runtime_directory", calibratorDir + id + "_RAW", calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "working_directory", calibratorDir + id + "_RAW", calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "pythonpath", pythonpath, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("remote", "max_per_node", max_per_node, calibratorDir + id + "_RAW" + "/pipeline.cfg")

        with open(calibratorDir + id + "_RAW" + '/Pre-Facet-Calibrator.parset', "r") as parset_file:
            parset_file = parset_file.readlines()

        for line in parset_file:
            if "! cal_input_path" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! cal_inp,ut_path          =  " + calibratorDir + id + "_RAW" + "  ## specify the directory where your calibrator data is stored\n")

            elif "! cal_input_pattern" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! cal_input_pattern       =  " + "L" + "*.MS"  +  "  ## regular expression pattern of all your calibrator files\n")

            elif "! prefactor_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! prefactor_directory      =  " + PrefactorDir + "  ## path to your prefactor copy\n")

            elif "! losoto_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! losoto_directory       =   " + losotopath + "  ## path to your local LoSoTo installation\n")

            elif "! aoflagger" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! aoflagger       =   " + aoflagger + "  ## path to your aoflagger executable\n")

            elif "! job_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! job_directory            = " + calibratorDirResults + " ## directory of the prefactor outputs\n")
            elif "! inspection_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! inspection_directory            = " + "{{ result_directory }}" + "cal_values_" + id + " ## directory of the prefactor outputs\n")
            elif "! cal_values_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! cal_values_directory            = " + "{{ result_directory }}" + "inspection_" + id + " ## directory of the prefactor outputs\n")

        with open(calibratorDir + id + "_RAW" + '/Pre-Facet-Calibrator.parset', "w") as parset_filew:
            parset_filew.write("".join(parset_file))

    for id in targetSASids:
        print("Setup for target id", id)
        createDirectory(targetDir + id + "_RAW")

        # Creating target files
        copyFiles(PrefactorDir + 'pipeline.cfg', targetDir + id + "_RAW")
        copyFiles(PrefactorDir + 'Pre-Facet-Target.parset', targetDir + id + "_RAW")
        setConfigs("DEFAULT", "lofarroot", lofarroot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "casaroot", casaroot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "pyraproot", pyraproot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "hdf5root", hdf5root, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "wcsroot", wcsroot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "runtime_directory", targetDir + id + "_RAW", targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "working_directory", targetDir + id + "_RAW", targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "pythonpath", pythonpath, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("remote", "max_per_node", max_per_node, targetDir + id + "_RAW"+ "/pipeline.cfg")

        with open(targetDir + id + "_RAW" + "/Pre-Facet-Target.parset", "r") as parset_file:
            parset_file = parset_file.readlines()

        for line in parset_file:
            if "! target_input_path" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! target_input_path          =  " + targetDir + id + "_RAW" + "  ## specify the directory where your target data is stored\n")

            elif "! target_input_pattern" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! target_input_pattern       =  " + "L" + "*.MS" + "  ## regular expression pattern of all your calibrator files\n")

            elif "! prefactor_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! prefactor_directory      =  " + PrefactorDir + "  ## path to your prefactor copy\n")

            elif "! losoto_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! losoto_directory       =   " + losotopath + "  ## path to your local LoSoTo installation\n")

            elif "! aoflagger" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! aoflagger       =   " + aoflagger + "  ## path to your aoflagger executable\n")

            elif "! cal_solutions" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! cal_solutions       =   " +  calibratorDirResults + "/cal_values_" + str(SASidsCalibrator[targetSASids.index(id)]) + "/cal_solutions.h5 \n")

            elif "! job_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! job_directory            =  " + targetDirResults + "  ## directory of the prefactor outputs\n")
            elif "! inspection_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! inspection_directory            = " + "{{ result_directory }}" + "cal_values_" + id + " ## directory of the prefactor outputs\n")
            elif "! cal_values_directory" in line:
                parset_file[parset_file.index(line)] = line.replace(line, "! cal_values_directory            = " + "{{ result_directory }}" + "inspection_" + id + " ## directory of the prefactor outputs\n")

        with open(targetDir + id + "_RAW" + "/Pre-Facet-Target.parset", "w") as parset_filew:
            for line in parset_file:
                parset_filew.write(line)

    print("Done")
    sys.exit(0)
