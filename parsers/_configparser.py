try:
    import configparser

except:
    import Configparser

def getConfigs(key, value, configFilePath):
    config = configparser.RawConfigParser()
    config.read(configFilePath)
    return config.get(key, value)