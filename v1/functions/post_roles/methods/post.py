import os
import json
import requests
from jwt import decode
from .contrib.db import db
from .contrib.utils import create_random_key

TYPES = ('author', 'assistant')
SECRET = os.environ.get('SECRET') or 'SECRET'
STATUSES = ('pending', 'request', 'active')


def post(e={}, context=None):
    data = None
    meta = None
    message = None
    status_code = 201

    try:
        jwt = e.get('headers', {}).get('Authorization')[4:]
        decoded = decode(jwt, SECRET, algorithm='HS256')
    except:
        return None, None, 'invalid auth token', 401

    try:
        body = json.loads(e.get('body'))
    except:
        body = {}

    type_ = body.get('type')
    secret = body.get('secret')
    user_id = body.get('user_id')
    post_key = body.get('post_key')

    if secret:
        role = (
            db.table('post_role')
            .where('secret', secret)
            .first()
        )

        if not role:
            return None, None, 'invalid secret', 401

        if role['user_id']:
            return None, None, 'already granted role', 401

        (
            db.table('post_role')
            .where('id', role['id'])
            .update({
                'status': 'active',
                'user_id': decoded['user_id'],
            })
        )

        data = (
            db.table('post_role')
            .where('id', role['id'])
            .first()
        )

        return data, None, None, 200

    is_admin = (
        db.table('user_role')
        .where('type', 'admin')
        .where('status', 'active')
        .where('user_id', decoded['user_id'])
        .count()
    ) > 0

    is_author = (
        db.table('post_role')
        .where('type', 'author')
        .where('status', 'active')
        .where('post_key', post_key)
        .where('user_id', decoded['user_id'])
        .count()
    ) > 0

    if type_ not in TYPES:
        return None, None, 'params is invalid or the value is empty', 403

    # 관리자 또는 작가만 새로운 역할을 부여할 수 있다.
    if not is_admin and not is_author:
        return None, None, 'no permission', 401

    if user_id:
        role_id = (
            db.table('post_role')
            .insert_get_id({
                'type': type_,
                'status': 'active',
                'user_id': user_id,
                'post_key': post_key,
                'grantor_id': decoded['user_id'],
            })
        )
    else:
        role_id = (
            db.table('post_role')
            .insert_get_id({
                'type': type_,
                'status': 'pending',
                'secret': create_random_key(length=150),
                'post_key': post_key,
                'grantor_id': decoded['user_id'],
            })
        )

    data = db.table('post_role').where('id', role_id).first()

    if os.environ.get('PYTEST_CURRENT_TEST'):  # 테스트 더미 데이터가 쌓이는 것을 방지한다.
        href = 'test'
    else:
        href = 'https://www.wearescdc.com/posts/{}/invite?secret={}'.format(post_key, data['secret'])  # noqa: E501

    res = requests.post('https://scdc.co', data=json.dumps({'href': href})).json()  # noqa: E501
    data['link'] = (res.get('data') or {}).get('link')

    return data, meta, message, status_code
