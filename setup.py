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
    auxDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/aux"
    logDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/logs"
    targetName = getConfigs("Data", "TargetName","config.cfg")
    workingDir = workingDir + "/" + targetName + "/"
    PrefacorDir = getConfigs("Paths", "PrefacorPath", "config.cfg")
    SASids = getConfigs("Data", "SASids", "config.cfg").replace(" ", "").split(",")

    home = str(Path.home())
    workingDir = workingDir.replace("$HOME", home)
    PrefacorDir = PrefacorDir.replace("$HOME", home)

    createDirectory(workingDir)
    createDirectory(auxDir)
    createDirectory(logDir)

    lofarroot = getConfigs("Paths", "lofarroot", "config.cfg")
    casaroot = getConfigs("Paths", "casaroot", "config.cfg")
    pyraproot = getConfigs("Paths", "pyraproot", "config.cfg")
    hdf5root = getConfigs("Paths", "hdf5root", "config.cfg")
    wcsroot = getConfigs("Paths", "wcsroot", "config.cfg")
    losotopath = getConfigs("Paths", "losotoPath", "config.cfg")
    aoflagger = getConfigs("Paths", "aoflagger", "config.cfg")

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
        imagingParset = ParsetParser(workingDir + id + '/Imaging_deep' + "/Initial-Subtract.parset")
        imagingParset.parse()
        imagingParset.setParam("! data_input_path", workingDir + id + "/Imaging_deep")
        imagingParset.setParam("! data_input_pattern", "L" + str(int(id)) + "*.ms")
        imagingParset.setParam("! prefactor_directory", PrefacorDir)
        imagingParset.setParam("! wsclean_executable", "/home/drabent/wsclean")
        imagingParset.setParam("! lofar_directory", "$LOFARROOT")
        imagingParset.setParam("! job_directory", "input.output.job_directory")
        imagingParset.setParam("! scripts", "{{prefactor_directory}}/scripts")
        imagingParset.setParam("pipeline.pluginpath", "{{prefactor_directory}}/plugins")
        imagingParset.setParam("! results_directory ", workingDir + id +'/Imaging_deep')
        imagingParset.setParam("! inspection_directory", workingDir + id +'/Imaging_deep')
        imagingParset.setParam("! local_scratch_dir", " /tmp")
        imagingParset.writeParset(workingDir + id + '/Imaging_deep' + "/Initial-Subtract.parset")

        # Creating calibrator files
        copyFiles(PrefacorDir + 'pipeline.cfg', workingDir + id + '/calibrators/')
        copyFiles(PrefacorDir + 'Pre-Facet-Calibrator.parset',  workingDir + id + '/calibrators/')
        setConfigs("DEFAULT", "runtime_directory", workingDir + id + "/calibrators/",workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "lofarroot", lofarroot, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "casaroot", casaroot, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "pyraproot", pyraproot, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "hdf5root", hdf5root, workingDir + id + '/calibrators/pipeline.cfg')
        setConfigs("DEFAULT", "wcsroot", wcsroot, workingDir + id + '/calibrators/pipeline.cfg')
        calibratorParset = ParsetParser(workingDir + id + '/calibrators/Pre-Facet-Calibrator.parset')
        calibratorParset.parse()
        calibratorParset.setParam("! cal_input_path", workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_' + calibratorNames[index]+ '')
        calibratorParset.setParam("! cal_input_pattern", "L" + str(int(id)) + "*.ms")
        calibratorParset.setParam("! prefactor_directory", PrefacorDir)
        calibratorParset.setParam("losoto_directory", losotopath)
        calibratorParset.setParam("! aoflagger", aoflagger)

        '''
        calibratorParset.setParam("! job_directory", "input.output.job_directory")
        calibratorParset.setParam("! scripts", "{{prefactor_directory}}/scripts")
        calibratorParset.setParam("pipeline.pluginpath", "{{prefactor_directory}}/plugins")
        calibratorParset.setParam("! results_directory ", workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_RESULTS')
        calibratorParset.setParam("! inspection_directory", workingDir + id + '/calibrators/L' + str(int(id) - 1) + '_RESULTS')
        calibratorParset.setParam("! local_scratch_dir", " /tmp")
        calibratorParset.writeParset(workingDir + id + '/calibrators/Pre-Facet-Calibrator.parset')
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
        targetParset.setParam("! job_directory", "input.output.job_directory")
        targetParset.setParam("! scripts", "{{prefactor_directory}}/scripts")
        targetParset.setParam("pipeline.pluginpath", "{{prefactor_directory}}/plugins")
        targetParset.setParam("! results_directory ",workingDir + id + '/targets/L' + str(int(id) - 1) + '_RESULTS')
        targetParset.setParam("! inspection_directory",workingDir + id + '/targets/L' + str(int(id) - 1) + '_RESULTS')
        targetParset.setParam("! local_scratch_dir", " /tmp")
        targetParset.writeParset(workingDir + id + '/targets/Pre-Facet-Target.parset')
        '''

        index += 1

    print("Done")




