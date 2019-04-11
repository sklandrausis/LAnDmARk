import configparser

class ConfigParser():
    __instance = None
    
    @staticmethod 
    def getInstance():
        if ConfigParser.__instance == None:
            ConfigParser()
        return ConfigParser.__instance
    
    def __init__(self):
        if ConfigParser.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ConfigParser.__instance = self
            
    def CreateConfig(self, configFilePath):
        self.configFilePath = configFilePath
        __config = configparser.RawConfigParser()
        __config.read(configFilePath)
        self.config = __config
          
    def getConfig(self, key, value):
        _config = self.config.get(key, value)
        return _config
    