import unittest
from python.methods.get_by_id import get_by_id


class GetByIdSuite(unittest.TestCase):
    def test_get(self):
        data, meta, message, status_code = get_by_id()

        self.assertEqual(data, None)
        self.assertEqual(meta, None)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 200)
