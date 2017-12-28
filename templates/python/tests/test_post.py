import unittest
from python.methods.post import post


class PostSuite(unittest.TestCase):
    def test_post(self):
        data, meta, message, status_code = post()

        self.assertEqual(data, None)
        self.assertEqual(meta, None)
        self.assertEqual(message, None)
        self.assertEqual(status_code, 201)
