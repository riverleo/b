import os
import json
from jwt import decode
from .contrib.db import db
from .contrib.utils import create_random_key

TYPES = ('admin', 'author')
SECRET = os.environ.get('SECRET') or 'SECRET'


def post(e={}):
    data = None
    meta = None
    message = None
    status_code = 403

    try:
        jwt = e.get('headers', {}).get('Authorization')[4:]
        decoded = decode(jwt, SECRET, algorithm='HS256')
    except:
        return None, None, 'invalid auth token', 401

    try:
        body = json.loads(e.get('body'))
    except:
        body = {}

    secret = body.get('secret')
    is_admin = (
        db.table('user_role')
        .where('type', 'admin')
        .where('status', 'active')
        .where('user_id', decoded['user_id'])
        .count()
    ) > 0

    if secret:  # 초대장을 받고 접근한 경우
        role = (
            db.table('user_role')
            .where('secret', secret)
            .first()
        )

        if not role:  # 존재하지 않는 시크릿 키'
            return None, None, 'invalid secret', 401

        exists_role = (
            db.table('user_role')
            .where('user_id', decoded['user_id'])
            .where('type', role.get('type'))
            .where('status', 'active')
            .first()
        )

        if exists_role:  # 이미 글을 쓸 수 있는 권한이 있는 경우
            return None, None, 'already exists role ({})'.format(role['type']), 401

        if role['user_id']:
            return None, None, 'already granted role', 401

        ( db.table('user_role')
            .where('id', role['id'])
            .update({
                'status': 'active',
                'user_id': decoded['user_id'],
            })
        )

        for _ in range(3):  # 새로 초대받은 경우 기본적으로 3개의 신규 초대권을 발급해준다.
            (
                db.table('user_role')
                .insert(
                    type='author',
                    grantor_id=decoded['user_id'],
                    secret=create_random_key(length=150),
                )
            )

        data = (
            db.table('user_role')
            .where('id', role['id'])
            .first()
        )
        status_code = 201
    elif is_admin:
        count = min(int(body.get('count', 1)), 5)  # 한번에 5개 이하의 초대장만 줄 수 있다.
        user_id = body.get('user_id')
        type_ = body.get('type') or 'author'
        grantor_id = body.get('grantor_id')

        if not user_id and not grantor_id:
            return None, None, 'must provide user_id or grantor_id', 403

        if user_id and grantor_id:
            return None, None, 'choose one of user_id and grantor_id', 403

        if user_id:
            id_ = db.table('user_role').insert_get_id({
                'user_id': user_id,
                'grantor_id': decoded['user_id'],
                'type': type_,
                'status': 'active',
            })

            data = db.table('user_role').where('id', id_).first()
        elif grantor_id:
            ids = []
            for _ in range(count):
                id_ = db.table('user_role').insert_get_id({
                    'grantor_id': grantor_id,
                    'type': type_,
                    'status': 'pending',
                    'secret': create_random_key(length=150),
                })
                ids.append(id_)

            data = db.table('user_role').where_in('id', ids).get()
        status_code = 201
    else:
        message = 'no secret'

    return data, meta, message, status_code
