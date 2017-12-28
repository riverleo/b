import unittest
from python.methods.get import get


class GetSuite(unittest.TestCase):
    def test_get(self):
        data, meta, message, status_code = get()

        self.assertEqual(data, None)
        self.assertEqual(meta, None)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 200)
