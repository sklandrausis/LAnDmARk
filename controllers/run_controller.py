from threading import Thread
from PyQt5.QtCore import QObject
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import numpy as np
from views.query_view import QueryView
from services.querying_service import Querying
from views.stage_progress_view import StageProgressPlot
from views.retrieve_progress_view import RetrieveProgressPlot
from views.process_view import ProcessView
from parsers._configparser import getConfigs

sns.set()
rcParams["font.size"] = 18
rcParams["legend.fontsize"] = "xx-large"
rcParams["ytick.major.size"] = 14
rcParams["xtick.major.size"] = 14
rcParams["axes.labelsize"] = 18


class RunController(QObject):
    def __init__(self, _ui, *args, **kwargs):
        super(RunController, self).__init__(*args, **kwargs)
        self.query_view = QueryView()
        self._ui = _ui
        self.config_file = "config.cfg"
        self.query_done = False
        self.done_color = "background-color: green"

    def query_progress(self):
        Thread(target=self.query_view.show()).start()

    def stage_progress(self):
        self.stage_progress_plot = StageProgressPlot(self._ui, self)
        Thread(target=self.stage_progress_plot.show()).start()

    def retrieve_progress(self):
        self.retrieve_progress_plot = RetrieveProgressPlot(self)
        Thread(target=self.retrieve_progress_plot.show()).start()

    def process_progress(self):
        self.process_progress_view = ProcessView()
        Thread(target=self.process_progress_view.show()).start()
