import unittest
from jwt import encode
from user_roles.methods.get import get
from user_roles.methods.post import SECRET
from user_roles.methods.contrib.db import db


class GetSuite(unittest.TestCase):
    def setUp(self):
        id_ = db.table('user').insert_get_id({'name': 'grantor'})
        jwt = encode({'user_id': id_}, SECRET, algorithm='HS256').decode('utf-8')  # noqa: E501

        self.grantor = db.table('user').where('id', id_).first()
        self.event = {
            'headers': {'Authorization': 'JWT {}'.format(jwt)},
        }

    def tearDown(Self):
        db.table('user').truncate()
        db.table('user_role').truncate()

    def test_fetching(self):
        data, _, _, _ = get(e=self.event)
        self.assertEqual(len(data), 0)

        db.table('user_role').insert(grantor_id=self.grantor['id'])

        data, _, _, _ = get(e=self.event)
        self.assertEqual(len(data), 1)

    def test_marshaling(self):
        db.table('user_role').insert(grantor_id=self.grantor['id'])

        data, _, _, _ = get(e=self.event)
        self.assertTrue('id' in data[0])
        self.assertTrue('user_id' in data[0])
        self.assertTrue('grantor_id' in data[0])
        self.assertTrue('secret' in data[0])
        self.assertTrue('status' in data[0])
        self.assertTrue('user' in data[0])
        self.assertTrue('grantor' in data[0])
        self.assertTrue('created_at' in data[0])
        self.assertTrue('updated_at' in data[0])

    def test_paging(self):
        for i in range(30):
            db.table('user_role').insert(grantor_id=self.grantor['id'])

        data, _, message, _ = get(self.event)
        self.assertEqual(message, None)
        self.assertEqual(len(data), 20)  # maximum data size is 20.

        e = self.event.copy()
        e.update({'queryStringParameters': {'per': '3'}})
        data, _, _, _ = get(e=e)
        self.assertEqual(len(data), 3)

        e = self.event.copy()
        e.update({'queryStringParameters': {'per': '100'}})
        data, _, _, _ = get(e=e)
        self.assertEqual(len(data), 20)  # max per is 20 even if exceed.

        e1 = self.event.copy()
        e1.update({'queryStringParameters': {'per': '10'}})
        e2 = self.event.copy()
        e2.update({'queryStringParameters': {'per': '3', 'page': '2'}})
        prev, _, _, _ = get(e=e1)
        data, _, _, _ = get(e=e2)
        self.assertEqual(prev[3], data[0])

        e = self.event.copy()
        e.update({'queryStringParameters': {'per': '100', 'page': '100'}})
        data, _, _, _ = get(e=e)
        self.assertEqual(len(data), 0)

    def test_status_filtering(self):
        db.table('user_role').insert(grantor_id=self.grantor['id'], status='pending')  # noqa: E501
        db.table('user_role').insert(grantor_id=self.grantor['id'], status='active')  # noqa: E501
        db.table('user_role').insert(grantor_id=self.grantor['id'], status='active')  # noqa: E501
        db.table('user_role').insert(grantor_id=self.grantor['id'], status='request')  # noqa: E501

        e = self.event.copy()
        e.update({'queryStringParameters': {'status': 'active'}})
        data, _, message, status_code = get(e=e)
        self.assertIsNone(message)
        self.assertEqual(status_code, 200)
        self.assertEqual(len(data), 2)

        e = self.event.copy()
        e.update({'queryStringParameters': {'status': 'request'}})
        data, _, _, _ = get(e=e)
        self.assertEqual(len(data), 1)

    def test_get_by_secret(self):
        db.table('user_role').insert(grantor_id=self.grantor['id'], secret='searched secret')  # noqa: E501
        db.table('user_role').insert(grantor_id=self.grantor['id'], secret='secret2')  # noqa: E501
        e = self.event.copy()
        e.update({'queryStringParameters': {'secret': 'searched secret'}})
        data, _, message, status_code = get(e=e)
        self.assertIsNone(message)
        self.assertEqual(status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['secret'], 'searched secret')

    def test_always_return_list(self):
        data, _, _, _ = get(self.event)

        self.assertEqual(type(data), list)
