import os
import argparse
from pathlib import Path

from parsers._configparser import setConfigs, getConfigs
from parsers._parsetParser import ParsetParser

def createDirectory(DirName):
    os.system("mkdir -p " + DirName)

def copyFiles(fileFrom, fileTo):
     os.system("cp -rfu " + fileFrom + "  " + fileTo)

def parseArguments():
    parser = argparse.ArgumentParser(description='''Setup working directory tree. ''', epilog="""Setup""")
    parser.add_argument("calibratorSources", help="calibrator sources", nargs="+", type=str, default="")
    parser.add_argument("-c", "--config", help="Configuration cfg file", type=str, default="config.cfg")
    parser.add_argument("-v", "--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args

def getArgs(key):
    return str(parseArguments().__dict__[key])

if __name__=="__main__":
    calibratorNames = getArgs("calibratorSources").replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(",")
    workingDir = getConfigs("Paths", "WorkingPath", "config.cfg")
    targetName = getConfigs("Data", "TargetName","config.cfg")
    workingDir = workingDir + targetName + "/"
    PrefactorDir = getConfigs("Paths", "PrefactorPath", "config.cfg")
    targetSASids = getConfigs("Data", "targetSASids", "config.cfg").replace(" ", "").split(",")

    home = str(Path.home())
    workingDir = workingDir.replace("$HOME", home)
    imagingDir = workingDir + "imaging_deep" + "/"
    calibratorDir = workingDir + "calibrators" + "/"
    targetDir = workingDir + "targets" + "/"
    auxDir = workingDir + "/Pipeline_aux"
    PrefactorDir = PrefactorDir.replace("$HOME", home)

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
        createDirectory(calibratorDir + id + "_" + calibratorNames[index])
        createDirectory(calibratorDir + id + "_RESULTS")
        createDirectory(targetDir + id + "_RAW")
        createDirectory(targetDir + id + "_RESULTS")

        # Creating calibrator files
        copyFiles(PrefactorDir + 'pipeline.cfg', calibratorDir)
        copyFiles(PrefactorDir + 'Pre-Facet-Calibrator.parset',  calibratorDir)
        setConfigs("DEFAULT", "lofarroot", lofarroot, calibratorDir + "pipeline.cfg")
        setConfigs("DEFAULT", "casaroot", casaroot, calibratorDir + "pipeline.cfg")
        setConfigs("DEFAULT", "pyraproot", pyraproot, calibratorDir + "pipeline.cfg")
        setConfigs("DEFAULT", "hdf5root", hdf5root, calibratorDir + "pipeline.cfg")
        setConfigs("DEFAULT", "wcsroot", wcsroot, calibratorDir + "pipeline.cfg")
        setConfigs("DEFAULT", "runtime_directory", calibratorDir, calibratorDir + "pipeline.cfg")
        setConfigs("DEFAULT", "working_directory", "%(runtime_directory)s", calibratorDir + "pipeline.cfg")
        setConfigs("remote", "max_per_node", max_per_node, calibratorDir + "pipeline.cfg")
        calibratorParset = ParsetParser(workingDir + id + '/calibrators/Pre-Facet-Calibrator.parset')

        calibratorParset.parse()
        calibratorParset.setParam("! cal_input_path", workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_' + calibratorNames[index]+ '')
        calibratorParset.setParam("! cal_input_pattern", "L" + str(int(id)) + "*.ms")
        calibratorParset.setParam("! prefactor_directory", PrefacorDir)
        calibratorParset.setParam("losoto_directory", losotopath)
        calibratorParset.setParam("! aoflagger", aoflagger)
        calibratorParset.writeParset(imagingDir + "/Initial-Subtract.parset")

        '''
        # Creating target files
        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id +'/targets/')
        copyFiles(PrefacorDir + 'Pre-Facet-Target.parset', workingDir + id +'/targets/')
        setConfigs("DEFAULT", "runtime_directory", workingDir + id + "/targets/", workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "lofarroot", lofarroot, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "casaroot", casaroot, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "pyraproot", pyraproot, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "hdf5root", hdf5root, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "wcsroot", wcsroot, workingDir + id + '/targets/pipeline.cfg')
        targetParset = ParsetParser(workingDir + id + '/targets/Pre-Facet-Target.parset')
        targetParset.parse()
        targetParset.setParam("! target_input_path", workingDir + id + '/targets/L' + str(int(id) - 1))
        targetParset.setParam("! target_input_pattern", "L" + str(int(id)) + "*.ms")
        targetParset.setParam("! prefactor_directory", PrefacorDir)
        targetParset.setParam("! losoto_directory", losotopath)
        targetParset.setParam("! aoflagger", aoflagger)
    
        '''
        index += 1

    print("Done")




