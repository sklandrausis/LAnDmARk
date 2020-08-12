import os
from operations.operation import Operation


class Stage(Operation):
    def __init__(self):
        Operation.__init__(self)
        self.__name = "stage"

    def execute(self):
        os.system("python3 operations/staging.py")

    @property
    def name(self):
        return self.__name
