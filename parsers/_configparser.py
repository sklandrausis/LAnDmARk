try:
    import configparser

except:
    import Configparser

def getConfigs(key, value, configFilePath):
    config = configparser.RawConfigParser()
    config.read(configFilePath)
    return config.get(key, value)

def setConfigs(section, key, value, configFilePath):
    config = configparser.RawConfigParser()
    config.read(configFilePath)
    config.set(section, key, value)

    with open(configFilePath, 'w') as configfile:
        config.write(configfile)

