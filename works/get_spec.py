import json
import unittest
from contrib import db
from get import handler


class GetSuite(unittest.TestCase):
    def setUp(self):
        db.table('work').truncate()
        db.table('user').truncate()
        db.table('workRole').truncate()

    def tearDown(self):
        db.table('work').truncate()
        db.table('user').truncate()
        db.table('workRole').truncate()

    def test_get(self):
        user_id = 'user'

        db.table('user').insert({'id': user_id})
        db.table('work').insert({'id': 'work1'})
        db.table('work').insert({'id': 'work2'})

        body = json.loads(handler({}, {}).get('body'))

        self.assertEqual(len(body.get('data')), 2)

    def test_get_by_author(self):
        user_id = 'user'
        work_id = 'work'

        db.table('user').insert({'id': user_id})
        db.table('work').insert({'id': work_id})
        db.table('work').insert({'id': 'work1'})
        db.table('work').insert({'id': 'work2'})
        db.table('work').insert({'id': 'work3'})
        db.table('workRole').insert({'userId': user_id, 'workId': work_id, 'type': 'author'})

        body = json.loads(handler({
            'queryStringParameters': {
                'authors': user_id,
            },
        }, {}).get('body'))

        self.assertEqual(len(body.get('data')), 1)
