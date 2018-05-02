import unittest
from orator.exceptions.query import QueryException
from contrib import db
from props import get_props, set_props


class PropsSuite(unittest.TestCase):
    def setUp(self):
        db.table('user').truncate()
        db.table('userRole').truncate()
        db.table('userProperty').truncate()

    def tearDown(self):
        db.table('user').truncate()
        db.table('userRole').truncate()
        db.table('userProperty').truncate()

    def test_get_props(self):
        set_props('id', props={'key': 'value'})
        prop = get_props('id', ['key', 'anonymous'])

        self.assertEqual(prop['key'], 'value')
        self.assertIsNone(prop['anonymous'])

    def test_set_props(self):
        set_props('id', props={'key': 'value'})
        prop = db.table('userProperty').first()

        self.assertEqual(prop.get('key'), 'key')
        self.assertEqual(prop.get('value'), 'value')
        self.assertTrue(prop.get('active'))
        self.assertIsNone(prop.get('unique'))

    def test_set_props_by_unique(self):
        set_props('user1', props={'key': 'unique_value'}, unique=True)

        self.assertEqual(db.table('userProperty').where({
            'userId': 'user1',
            'value': 'unique_value',
        }).count(), 1)

        # 다른 사용자가 유니크한 값을 사용할 수 없다.
        with self.assertRaises(QueryException):
            set_props('user2', props={'key': 'unique_value'}, unique=True)

        # 기존 사용자는 값을 변경할 수 있다.
        set_props('user1', props={'key': 'unique_another_value'}, unique=True)
        self.assertEqual(db.table('userProperty').where({
            'userId': 'user1',
            'value': 'unique_another_value',
        }).count(), 1)

        # 기존 사용자가 해당 값을 더이상 사용하지 않은 경우 변경 가능하다
        set_props('user2', props={'key': 'unique_value'}, unique=True)
        self.assertEqual(db.table('userProperty').where({
            'userId': 'user2',
            'value': 'unique_value',
        }).count(), 1)
