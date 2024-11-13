import unittest
import geoservices as ctc

class AddTests(unittest.TestCase):
    def test_one_plus_two(self):
        self.assertEqual(3, 1+2, 'The test has failed')
        
class CepToCoordsTests(unittest.TestCase):
    def test_coordinates_retrieval(self):
        self.assertEqual(ctc.getCoordsFromCep('50810000'), {'lat': '1', 'lng': '2'})