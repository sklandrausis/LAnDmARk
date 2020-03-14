#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication)
from controllers.main_controller import MainController
from views.main_view import MainView


class LandmarkGUI(QApplication):
    def __init__(self, sys_argv):
        super(LandmarkGUI, self).__init__(sys_argv)
        self.main_controller = MainController()
        self.main_view = MainView(self.main_controller)
        self.main_view.show()


def main():
    app = LandmarkGUI(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
