from PyQt5.QtCore import QObject


class CheckController(QObject):
    def __init__(self, *args, **kwargs):
        super(CheckController, self).__init__(*args, **kwargs)

    def check(self):
        print("check")