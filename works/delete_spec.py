import json
import unittest
from contrib import db, jwt_encode
from delete import handler


class DeleteSuite(unittest.TestCase):
    def setUp(self):
        db.table('work').truncate()
        db.table('workRole').truncate()

    def tearDown(self):
        db.table('work').truncate()
        db.table('workRole').truncate()

    def test_delete(self):
        user_id = 'user'
        work_id = 'work'

        db.table('work').insert({'id': work_id})
        db.table('workRole').insert({
            'userId': user_id,
            'workId': work_id,
            'type': 'author',
        })

        work = db.table('work').where('id', work_id).first()

        self.assertIsNone(work.get('deletedAt'))

        handler({
            'headers': {
                'Authorization': jwt_encode(user_id),
            },
            'pathParameters': {
                'id': work_id,
            },
        }, None)

        work = db.table('work').where('id', work_id).first()

        self.assertIsNotNone(work.get('deletedAt'))

    def test_delete_by_not_authorized(self):
        user_id = 'user'
        work_id = 'work'

        db.table('work').insert({'id': work_id})
        db.table('workRole').insert({
            'userId': user_id,
            'workId': work_id,
            'type': 'author',
        })

        work = db.table('work').where('id', work_id).first()

        self.assertIsNone(work.get('deletedAt'))

        body = json.loads(handler({
            'pathParameters': {'id': work_id},
        }, None)['body'])

        work = db.table('work').where('id', work_id).first()

        self.assertEqual(body['error']['code'], 2)
        self.assertEqual(body['error']['message'], 'no permissions')
        self.assertIsNone(work.get('deletedAt'))
