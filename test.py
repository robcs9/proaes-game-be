import unittest
import geoservices as ctc

class AddTests(unittest.TestCase):
    def test_one_plus_two(self):
        self.assertEqual(3, 1+2, 'The test has failed')
        
class CepToCoordsTests(unittest.TestCase):
    def test_coordinates_retrieval(self):
        # self.assertEqual(ctc.getCoordsFromCep('50810000'), {'lat': '1', 'lng': '2'})
        pass
    def test_batch_geocode(self):
        res = ctc.batchGeocode(['54330-075','54000-000','55000-000'])
        # aprint(res)