import unittest
from contrib import db, new_id, password


class ContribSuite(unittest.TestCase):
    def test_db(self):
        result = db.select('select 1 + 1 AS v')

        self.assertEqual(result[0]['v'], 2)

    def test_new_id(self):
        for _ in range(100):
            id1 = new_id()
            id2 = new_id()

            self.assertNotEqual(id1, id2)
            self.assertIsNotNone(id1)
            self.assertIsNotNone(id2)

    def test_password(self):
        self.assertNotEqual(password('password'), 'password')
        self.assertEqual(password('password'), password('password'))
        self.assertNotEqual(password('passwOrd'), password('password'))
        self.assertEqual(password('비밀번호'), password('비밀번호'))
        self.assertEqual(password('😘'), password('😘'))
