from threading import Thread
from PyQt5.QtCore import QObject
from views.query_view import QueryView
from views.stage_progress_view import StageProgressPlot
from views.retrieve_progress_view import RetrieveProgressPlot
from views.process_view import ProcessView


class RunController(QObject):
    def __init__(self, _ui, *args, **kwargs):
        super(RunController, self).__init__(*args, **kwargs)
        self._ui = _ui
        self.query_view = QueryView(self._ui)

    def query_progress(self):
        Thread(target=self.query_view.show()).start()

    def stage_progress(self):
        self.stage_progress_plot = StageProgressPlot(self._ui)
        Thread(target=self.stage_progress_plot.show()).start()

    def retrieve_progress(self):
        self.retrieve_progress_plot = RetrieveProgressPlot(self)
        Thread(target=self.retrieve_progress_plot.show()).start()

    def process_progress(self):
        self.process_progress_view = ProcessView()
        Thread(target=self.process_progress_view.show()).start()
