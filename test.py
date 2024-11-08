import unittest

class AddTests(unittest.TestCase):
    def test_one_plus_two(self):
        self.assertEqual(3, 1+2, 'The test has failed')