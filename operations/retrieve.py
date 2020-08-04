import os
from operations.operation import Operation


class Retrieve(Operation):
    def __init__(self):
        Operation.__init__(self)
        self.__name = "retrieve"

    def execute(self):
        os.system("python3 operations/retrieving.py")

    @property
    def name(self):
        return self.__name
