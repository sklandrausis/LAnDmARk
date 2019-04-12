import os

from parsers._configparser import ConfigParser

def getConfigs(key, value):
    configFilePath = "config.cfg"
    config = ConfigParser.getInstance()
    config.CreateConfig(configFilePath)
    return config.getConfig(key, value)

def createDirectory(DirName):
    os.system("mkdir " + DirName)

def copyFiles(fileFrom, fileTo):
    os.system("cp -rf " + fileFrom + "  " + fileTo)

if __name__=="__main__":
    workingDir = getConfigs("Paths", "WorkingPath")
    auxDir = getConfigs("Paths", "AuxPath")
    PrefacorDir = getConfigs("Paths", "PrefacorPath")
    SASid = getConfigs("Data", "SASid")
    calibratorName = getConfigs("Data", "CalibratorName")

    createDirectory(workingDir + "calibrators")
    createDirectory(workingDir + '/calibrators/L' + str(int(SASid[0]) - 1) + '_' + calibratorName+ '')
    createDirectory(workingDir + '/calibrators/L' + str(int(SASid[1]) - 1) + '_' + calibratorName+ '')
    createDirectory(workingDir + '/calibrators/L' + str(int(SASid[0]) - 1) + '_RESULTS')
    createDirectory(workingDir + '/calibrators/L' + str(int(SASid[1]) - 1) + '_RESULTS')
    createDirectory(workingDir + '/targets')
    createDirectory(workingDir + '/targets/L' + str(int(SASid[0])) + '')
    createDirectory(workingDir + '/targets/L' + str(int(SASid[1])) + '')
    createDirectory(workingDir + '/Pipeline_prefactor')
    createDirectory(workingDir + '/Imaging_deep')

    copyFiles(PrefacorDir + '/PARSETS/Imaging_deep-pipeline.cfg', workingDir + '/')
    copyFiles(PrefacorDir + '/PARSETS/Imaging_deep.parset', workingDir + '/')

    #copyFiles(auxDir + '/FILES/* ' + workingDir + '/calibrators/L' + str(int(SASid[0]) - 1) + '_' + str(calibratorName) + '')
    #copyFiles(auxDir + '/FILES/* ' + workingDir + '/calibrators/L' + str(int(SASid[1]) - 1) + '_' + str(calibratorName) + '')

    copyFiles(PrefacorDir + '/PARSETS/Pre-Facet-Calibrator-RawSingle-pipeline.cfg', workingDir + '/calibrators/')
    copyFiles(PrefacorDir + '/PARSETS/Pre-Facet-Calibrator-RawSingle.parset',  workingDir + '/calibrators/')

    #copyFiles(auxDir + '/FILES/* ' + workingDir + '/targets/L' + str(int(SASid[0])) + '')
    #copyFiles(auxDir + '/FILES/* ' + workingDir + '/targets/L' + str(int(SASid[1])) + '')

    copyFiles(PrefacorDir + '/PARSETS/Pre-Facet-Target-RawCombine-pipeline.cfg', workingDir + '/targets/')
    copyFiles(PrefacorDir + '/PARSETS/Pre-Facet-Target-RawCombine.parset', workingDir + '/targets/')

    #copyFiles(auxDir + '/SCRIPTS/runTARGET.py ' + workingDir + '/targets/')

    print("Done")




