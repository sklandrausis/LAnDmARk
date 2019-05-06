import unittest

from startStaging import Staging

class testStartStaging(unittest.TestCase):

    def setUp(self):
        # Tested SAS IDs 225554, 201522
        self.Staging_225554 = Staging([225554], False, "test225554_config.cfg")
        self.Staging_225554.query()

        self.Staging_201522 = Staging([201522], False, "test201522_config.cfg")
        self.Staging_201522.query()

    def testStationCount(self):
        #Testing 22554
        self.assertEqual(self.Staging_225554.getStationsCount()["core"], 23)
        self.assertEqual(self.Staging_225554.getStationsCount()["remote"], 14)
        self.assertEqual(self.Staging_225554.getStationsCount()["international"], 0)
        self.assertEqual(self.Staging_225554.getStationsCount()["total"], 37)

        #Testing 201522
        self.assertEqual(self.Staging_201522.getStationsCount()["core"], 23)
        self.assertEqual(self.Staging_201522.getStationsCount()["remote"], 14)
        self.assertEqual(self.Staging_201522.getStationsCount()["international"], 0)
        self.assertEqual(self.Staging_201522.getStationsCount()["total"], 37)

    def testValidFilesCount(self):
        #Testing 22554
        self.assertEqual(self.Staging_225554.getDataGoodnes()["225554"]["validFiles"], 79)
        self.assertEqual(self.Staging_225554.getDataGoodnes()["225554"]["invalidFiles"], 0)

        # Testing 201522
        self.assertEqual(self.Staging_201522.getDataGoodnes()["201522"]["validFiles"], 79)
        self.assertEqual(self.Staging_201522.getDataGoodnes()["201522"]["invalidFiles"], 1)


if __name__ == '__main__':
    unittest.main()