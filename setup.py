import os
import argparse
from pathlib import Path

from parsers._configparser import setConfigs, getConfigs

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
    auxDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/aux"
    logDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/logs"
    targetName = getConfigs("Data", "TargetName","config.cfg")
    workingDir = workingDir + "/" + targetName + "/"
    PrefacorDir = getConfigs("Paths", "PrefacorPath", "config.cfg")
    SASids = getConfigs("Data", "SASids", "config.cfg").replace(" ", "").split(",")

    home = str(Path.home())
    workingDir = workingDir.replace("$HOME", home)

    createDirectory(workingDir)
    createDirectory(auxDir)
    createDirectory(logDir)

    lofarroot = getConfigs("Paths", "lofarroot", "config.cfg")
    casaroot = getConfigs("Paths", "casaroot", "config.cfg")
    pyraproot = getConfigs("Paths", "pyraproot", "config.cfg")
    hdf5root = getConfigs("Paths", "hdf5root", "config.cfg")
    wcsroot = getConfigs("Paths", "wcsroot", "config.cfg")

    index = 0
    for id in SASids:
        print ("id", id)

        createDirectory(workingDir + id)
        createDirectory(workingDir + id +'/calibrators/' )
        createDirectory(workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_' + calibratorNames[index]+ '')
        createDirectory(workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_RESULTS')
        createDirectory(workingDir + id + '/targets')
        createDirectory(workingDir + id + '/targets/L' + str(int(id)) + '')
        createDirectory(workingDir + id +'/Imaging_deep')

        # Creating imaging files
        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id + '/Imaging_deep')
        copyFiles(PrefacorDir + 'Initial-Subtract.parset', workingDir + id + '/Imaging_deep')
        setConfigs("DEFAULT", "runtime_directory", workingDir + id + "/Imaging_deep/", workingDir + id + '/Imaging_deep/pipeline.cfg')
        setConfigs("DEFAULT", "lofarroot", lofarroot, workingDir + id + '/Imaging_deep/pipeline.cfg')
        setConfigs("DEFAULT", "casaroot", casaroot, workingDir + id + '/Imaging_deep/pipeline.cfg')
        setConfigs("DEFAULT", "pyraproot", pyraproot, workingDir + id + '/Imaging_deep/pipeline.cfg')
        setConfigs("DEFAULT", "hdf5root", hdf5root, workingDir + id + '/Imaging_deep/pipeline.cfg')
        setConfigs("DEFAULT", "wcsroot", wcsroot, workingDir + id + '/Imaging_deep/pipeline.cfg')

        # Creating calibrator files
        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id + '/calibrators/')
        copyFiles(PrefacorDir + 'Pre-Facet-Calibrator.parset',  workingDir + id + '/calibrators/')
        setConfigs("DEFAULT", "runtime_directory", workingDir + id + "/calibrators/",workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "lofarroot", lofarroot, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "casaroot", casaroot, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "pyraproot", pyraproot, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "hdf5root", hdf5root, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "wcsroot", wcsroot, workingDir + id + '/calibrators/pipeline.cfg')


        # Creating target files
        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id +'/targets/')
        copyFiles(PrefacorDir + 'Pre-Facet-Target.parset', workingDir + id +'/targets/')
        setConfigs("DEFAULT", "runtime_directory", workingDir + id + "/targets/", workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "lofarroot", lofarroot, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "casaroot", casaroot, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "pyraproot", pyraproot, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "hdf5root", hdf5root, workingDir + id + '/targets/pipeline.cfg')
        setConfigs("DEFAULT", "wcsroot", wcsroot, workingDir + id + '/targets/pipeline.cfg')

        index += 1

    print("Done")




