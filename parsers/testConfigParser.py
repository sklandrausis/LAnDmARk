import unittest

from _configparser import ConfigParser

class TestConfigParser(unittest.TestCase):
    
    def test_canCreateCreateOnlyOneObject(self):
        
        s1 = ConfigParser.getInstance()
        s2 = ConfigParser.getInstance()
        self.assertEqual(str(s1), str(s2))
        
    def test_creatingObjectsErrorIsRaise(self):
        self.assertRaises(Exception, ConfigParser)
    
    def test_getConfig(self):
        configFilePath = "/home/janis/Documents/workspace-sts/DataProcessingForMaserObservation/config/config.cfg"
        s1 = ConfigParser.getInstance()
        s1.CreateConfig(configFilePath)
        self.assertEqual(s1.getConfig("paths", "logPath"), "logs/")
        self.assertEqual(s1.getConfig("velocities", "cepa"), "-1.77, -2.41, -3.66, -4.01, -4.67")
        self.assertEqual(s1.getConfig("sources", "ec53"), "182951.2, 011638.0, 2000.0")
    
if __name__ == '__main__':
    unittest.main()