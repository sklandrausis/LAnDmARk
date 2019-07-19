import os
import argparse

from parsers._configparser import setConfigs, getConfigs
from parsers._parsetParser import ParsetParser

def createDirectory(DirName):
    os.system("mkdir -p " + DirName)

def copyFiles(fileFrom, fileTo):
     os.system("cp -rfu " + fileFrom + "  " + fileTo)

def parseArguments():
    parser = argparse.ArgumentParser(description='''Setup working directory tree. ''', epilog="""Setup""")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args

def getArgs(key):
    return str(parseArguments().__dict__[key])

if __name__=="__main__":
    workingDir = getConfigs("Paths", "WorkingPath", "config.cfg")
    targetName = getConfigs("Data", "TargetName","config.cfg")
    workingDir = workingDir + targetName + "/"
    PrefactorDir = getConfigs("Paths", "PrefactorPath", "config.cfg")
    targetSASids = getConfigs("Data", "targetSASids", "config.cfg").replace(" ", "").split(",")

    imagingDir = workingDir + "imaging_deep" + "/"
    calibratorDir = workingDir + "calibrators" + "/"
    targetDir = workingDir + "targets" + "/"
    auxDir = workingDir + "/Pipeline_aux"

    # Creating directory structure
    createDirectory(workingDir)
    createDirectory(imagingDir)
    createDirectory(calibratorDir)
    createDirectory(targetDir)
    createDirectory(auxDir)

    lofarroot = getConfigs("Paths", "lofarroot", "config.cfg")
    casaroot = getConfigs("Paths", "casaroot", "config.cfg")
    pyraproot = getConfigs("Paths", "pyraproot", "config.cfg")
    hdf5root = getConfigs("Paths", "hdf5root", "config.cfg")
    wcsroot = getConfigs("Paths", "wcsroot", "config.cfg")
    losotopath = getConfigs("Paths", "losotoPath", "config.cfg")
    aoflagger = getConfigs("Paths", "aoflagger", "config.cfg")
    max_per_node = getConfigs("Data", "max_per_node", "config.cfg")
    wsclean_executable = getConfigs("Paths", "wsclean_executable", "config.cfg")

    # Creating imaging files
    copyFiles(PrefactorDir + 'pipeline.cfg', imagingDir)
    copyFiles(PrefactorDir + 'Initial-Subtract.parset', imagingDir)
    setConfigs("DEFAULT", "lofarroot", lofarroot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "casaroot", casaroot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "pyraproot", pyraproot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "hdf5root", hdf5root, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "wcsroot", wcsroot, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "runtime_directory", imagingDir, imagingDir + "pipeline.cfg")
    setConfigs("DEFAULT", "working_directory", "%(runtime_directory)s", imagingDir + "pipeline.cfg")
    setConfigs("remote", "max_per_node", max_per_node, imagingDir + "pipeline.cfg")
    imagingParset = ParsetParser(imagingDir + "/Initial-Subtract.parset")
    imagingParset.parse()
    imagingParset.setParam("! data_input_path", targetDir)
    imagingParset.setParam("! data_input_pattern", "L" + "*.pre-cal.ms")
    imagingParset.setParam("! prefactor_directory", PrefactorDir)
    imagingParset.setParam("! wsclean_executable", wsclean_executable)
    imagingParset.writeParset(imagingDir + "/Initial-Subtract.parset")

    index = 0
    for id in targetSASids:
        print ("Setup for target id", id)
        createDirectory(calibratorDir + id + "_RAW")
        createDirectory(calibratorDir + id + "_RESULTS")
        createDirectory(targetDir + id + "_RAW")
        createDirectory(targetDir + id + "_RESULTS")

        # Creating calibrator files
        copyFiles(PrefactorDir + 'pipeline.cfg', calibratorDir + id + "_RAW/")
        copyFiles(PrefactorDir + 'Pre-Facet-Calibrator.parset',  calibratorDir + id + "_RAW/")
        setConfigs("DEFAULT", "lofarroot", lofarroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "casaroot", casaroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "pyraproot", pyraproot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "hdf5root", hdf5root, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "wcsroot", wcsroot, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "runtime_directory", calibratorDir + id + "_RAW", calibratorDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "working_directory", calibratorDir + id + "_RAW", calibratorDir + id + "_RAW" + "/pipeline.cfg"
        setConfigs("remote", "max_per_node", max_per_node, calibratorDir + id + "_RAW" + "/pipeline.cfg")
        calibratorParset = ParsetParser(calibratorDir + id + "_RAW" + '/Pre-Facet-Calibrator.parset')
        calibratorParset.parse()
        calibratorParset.setParam("! cal_input_path", calibratorDir + id + "_RAW"+ '')
        calibratorParset.setParam("! cal_input_pattern",  "L" + "*.MS")
        calibratorParset.setParam("! prefactor_directory", PrefactorDir)
        calibratorParset.setParam("! losoto_directory", losotopath)
        calibratorParset.setParam("! aoflagger", aoflagger)
        calibratorParset.setParam("! job_directory", calibratorDir + id + "_RESULTS")
        calibratorParset.writeParset(calibratorDir + id + "_RAW" + '/Pre-Facet-Calibrator.parset')

        # Creating target files
        copyFiles(PrefactorDir + 'pipeline.cfg', targetDir + id + "_RAW")
        copyFiles(PrefactorDir + 'Pre-Facet-Target.parset', targetDir + id + "_RAW")
        setConfigs("DEFAULT", "lofarroot", lofarroot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "casaroot", casaroot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "pyraproot", pyraproot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "hdf5root", hdf5root, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "wcsroot", wcsroot, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "runtime_directory", targetDir, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("DEFAULT", "working_directory", targetDir, targetDir + id + "_RAW" + "/pipeline.cfg")
        setConfigs("remote", "max_per_node", max_per_node, targetDir + id + "_RAW"+ "/pipeline.cfg")
        targetParset = ParsetParser(targetDir + id + "_RAW/" + 'Pre-Facet-Target.parset')
        targetParset.parse()
        targetParset.setParam("! target_input_path", targetDir + id + "_RAW")
        targetParset.setParam("! target_input_pattern", "L" + "*.MS")
        targetParset.setParam("! prefactor_directory", PrefactorDir)
        targetParset.setParam("! losoto_directory", losotopath)
        targetParset.setParam("! aoflagger", aoflagger)
        targetParset.setParam("! cal_solutionsr", calibratorDir + id + "_RESULTS" + "/cal_values/cal_solutions.h5")
        targetParset.setParam("! job_directory", targetDir + id + "_RESULTS")
        targetParset.writeParset(targetDir + id + "_RAW/" + 'Pre-Facet-Target.parset')

        index += 1

    print("Done")
