import os
import argparse

from parsers._configparser import getConfigs

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
    calibratorNames

    workingDir = getConfigs("Paths", "WorkingPath", "config.cfg")
    auxDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/aux"
    logDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/logs"
    targetName = getConfigs("Data", "TargetName","config.cfg")
    workingDir = workingDir + "/" + targetName + "/"
    PrefacorDir = getConfigs("Paths", "PrefacorPath", "config.cfg")
    SASids = getConfigs("Data", "SASids", "config.cfg").replace(" ", "").split(",")

    createDirectory(workingDir)
    createDirectory(auxDir)
    createDirectory(logDir)

    index = 0
    for id in SASids:
        print ("id", id)

        createDirectory(workingDir + id)
        createDirectory(workingDir + id +'/calibrators/' )
        createDirectory(workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_' + calibratorNames[index]+ '')
        createDirectory(workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_RESULTS')
        createDirectory(workingDir + id + '/targets')
        createDirectory(workingDir + id + '/targets/L' + str(int(id)) + '')
        createDirectory(workingDir + id + '/Pipeline_prefactor')
        createDirectory(workingDir + id +'/Imaging_deep')

        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id + '/')
        copyFiles(PrefacorDir + 'Imaging.parset', workingDir + id + '/')

        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id + '/calibrators/')
        copyFiles(PrefacorDir + 'Pre-Facet-Calibrator.parset',  workingDir + id + '/calibrators/')

        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id +'/targets/')
        copyFiles(PrefacorDir + 'Pre-Facet-Target.parset', workingDir + id +'/targets/')
        index += 1

    print("Done")




