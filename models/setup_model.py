from PyQt5.QtCore import QObject


class SetupModel(QObject):
    def __init__(self):
        super().__init__()
        self.__querying = "True"
        self.__stage = "False"
        self.__retrieve = "False"
        self.__process = "False"
        self.__which_obj = "calibrators"
        self.__calibratorSASids = []
        self.__targetSASids = []
        self.__Target_name = ""
        self.__PROJECTid = "MSSS_HBA_2013"
        self.__product_type = "observation"
        self.__max_per_node = 20
        self.__method = "local"
        self.__WorkingPath = "/home/janis/Documents/msss"
        self.__PrefactorPath = "/home/janis/Documents/prefactor"
        self.__lofarroot = "/opt/cep/lofim/daily/Tue/lofar_build/install/gnucxx11_opt"
        self.__casaroot = "/opt/cep/casacore/casacore_current"
        self.__pyraproot = "/opt/cep/casacore/python-casacore_current/lib64/python2.7/site-packages"
        self.__hdf5root = ""
        self.__wcsroot = ""
        self.__losotoPath = "/data/scratch/iacobelli/losoto_Nov21_latest_commit_a7790a6/"
        self.__aoflagger = "/opt/cep/aoflagger/aoflagger-2.10.0/build/bin/aoflagger"
        self.__wsclean_executable = "/opt/cep/wsclean/wsclean-2.8/bin/wsclean"
        self.__pythonpath = ""
        self.__task_file = "%(lofarroot)s/share/pipeline/tasks.cfg"
        self.__max_subband = ""
        self.__min_subband = ""
        self.__subband_select = "False"

    @property
    def querying(self):
        return self.__querying

    @querying.setter
    def querying(self, querying):
        self.__querying = querying

    @property
    def stage(self):
        return self.__stage

    @stage.setter
    def stage(self, stage):
        self.__stage = stage

    @property
    def retrieve(self):
        return self.__retrieve

    @retrieve.setter
    def retrieve(self, retrieve):
        self.__retrieve = retrieve

    @property
    def process(self):
        return self.__process

    @process.setter
    def process(self, process):
        self.__process = process

    @property
    def which_obj(self):
        return self.__which_obj

    @which_obj.setter
    def which_obj(self, which_obj):
        self.__which_obj = which_obj

    @property
    def calibratorSASids(self):
        return self.__calibratorSASids

    @calibratorSASids.setter
    def calibratorSASids(self, calibratorSASids):
        self.__calibratorSASids = calibratorSASids

    @property
    def targetSASids(self):
        return self.__targetSASids

    @targetSASids.setter
    def targetSASids(self, targetSASids):
        self.__targetSASids = targetSASids

    @property
    def Target_name(self):
        return self.__Target_name

    @Target_name.setter
    def Target_name(self, Target_name):
        self.__Target_name = Target_name

    @property
    def PROJECTid(self):
        return self.__PROJECTid

    @PROJECTid.setter
    def PROJECTid(self, PROJECTid):
        self.__PROJECTid = PROJECTid

    @property
    def product_type(self):
        return self.__product_type

    @product_type.setter
    def product_type(self, product_type):
        self.__product_type = product_type

    @property
    def max_per_node(self):
        return self.__max_per_node

    @max_per_node.setter
    def max_per_node(self, max_per_node):
        self.__max_per_node = max_per_node

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def WorkingPath(self):
        return self.__WorkingPath

    @WorkingPath.setter
    def WorkingPath(self, WorkingPath):
        self.__WorkingPath = WorkingPath

    @property
    def PrefactorPath(self):
        return self.__PrefactorPath

    @PrefactorPath.setter
    def PrefactorPath(self, PrefactorPath):
        self.__PrefactorPath = PrefactorPath

    @property
    def lofarroot(self):
        return self.__lofarroot

    @lofarroot.setter
    def lofarroot(self, lofarroot):
        self.__lofarroot = lofarroot

    @property
    def casaroot(self):
        return self.__casaroot

    @casaroot.setter
    def casaroot(self, casaroot):
        self.__casaroot = casaroot

    @property
    def pyraproot(self):
        return self.__pyraproot

    @pyraproot.setter
    def pyraproot(self, pyraproot):
        self.__pyraproot = pyraproot

    @property
    def hdf5root(self):
        return self.__hdf5root

    @hdf5root.setter
    def hdf5root(self, hdf5root):
        self.__hdf5root = hdf5root

    @property
    def wcsroot(self):
        return self.__wcsroot

    @wcsroot.setter
    def wcsroot(self, wcsroot):
        self.__wcsroot = wcsroot

    @property
    def losotoPath(self):
        return self.__losotoPath

    @losotoPath.setter
    def losotoPath(self, losotoPath):
        self.__losotoPath = losotoPath

    @property
    def aoflagger(self):
        return self.__aoflagger

    @aoflagger.setter
    def aoflagger(self, aoflagger):
        self.__aoflagger = aoflagger

    @property
    def wsclean_executable(self):
        return self.__wsclean_executable

    @wsclean_executable.setter
    def wsclean_executable(self, wsclean_executable):
        self.__wsclean_executable = wsclean_executable

    @property
    def pythonpath(self):
        return self.__pythonpath

    @pythonpath.setter
    def pythonpath(self, pythonpath):
        self.__pythonpath = pythonpath

    @property
    def task_file(self):
        return self.__task_file

    @task_file.setter
    def task_file(self, task_file):
        self.__task_file = task_file

    @property
    def min_subband(self):
        return self.__min_subband

    @min_subband.setter
    def min_subband(self, min_subband):
        self.__min_subband = min_subband

    @property
    def max_subband(self):
        return self.__max_subband

    @max_subband.setter
    def max_subband(self, max_subband):
        self.__max_subband = max_subband

    @property
    def subband_select(self):
        return self.__subband_select

    @subband_select.setter
    def subband_select(self, subband_select):
        self.__subband_select = subband_select
