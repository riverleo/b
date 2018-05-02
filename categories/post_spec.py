import json
import unittest
from contrib import db
from post import handler


class PostSuite(unittest.TestCase):
    def setUp(self):
        db.table('category').truncate()
        db.table('categoryMap').truncate()

    def tearDown(self):
        db.table('category').truncate()
        db.table('categoryMap').truncate()

    def test_post(self):
        keys = ['category1', 'category2']

        handler({'body': json.dumps({'keys': keys})}, None)

        self.assertEqual(db.table('category').lists('key'), keys)
        self.assertEqual(db.table('categoryMap').count(), 0)

    def test_post_with_categorizable(self):
        keys = ['category1', 'category2']

        handler({'body': json.dumps({
            'keys': keys,
            'categorizableId': 'id',
            'categorizableType': 'work',
        })}, None)

        self.assertEqual(db.table('category').lists('key'), keys)
        self.assertEqual(db.table('categoryMap').count(), 2)

        keys = ['category1', 'category3', 'category4']

        handler({'body': json.dumps({
            'keys': keys,
            'categorizableId': 'id',
            'categorizableType': 'work',
        })}, None)

        total_keys = ['category1', 'category2', 'category3', 'category4']
        self.assertEqual(db.table('category').lists('key'), total_keys)
        self.assertEqual(db.table('categoryMap').count(), 3)
