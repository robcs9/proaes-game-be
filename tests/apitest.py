import unittest, requests as rq

IGNORE_TESTS = True

@unittest.skipIf(IGNORE_TESTS, 'API inativa')
class ApiTests(unittest.TestCase):
  def test_api_root(self):
    res = rq.get('http://localhost:8000/api/v1')
    self.assertEqual(res.status_code, 200)