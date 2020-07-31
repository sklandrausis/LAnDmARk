import os
from operations.operation import Operation


class Query(Operation):
    def __init__(self):
        Operation.__init__(self)
        self.__name = "query"

    def execute(self):
        os.system("python3 operations/querying.py")

    @property
    def name(self):
        return self.__name
