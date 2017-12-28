import os
from jwt import encode, decode
from .contrib.db import db

SECRET = os.environ.get('SECRET') or 'SECRET'


def get(e={}):
    data = None
    meta = None
    message = None
    status_code = 200

    try:
        jwt = e.get('headers', {}).get('Authorization')[4:]
        decoded = decode(jwt, SECRET, algorithm='HS256')
    except:
        return None, None, 'invalid auth token', 401

    fields = ('id', 'name', 'email', 'lang', 'country', 'created_at')
    data = (
        db.table('user')
        .select(*fields)
        .where('id', decoded['user_id'])
        .first()
    )

    if not data:
        return None, 'invalid auth token', 401

    data['jwt'] = encode({'user_id': data['id']}, SECRET, algorithm='HS256').decode('utf-8')
    data['roles'] = (
        db.table('user_role')
        .or_where('user_id', decoded['user_id'])
        .or_where('grantor_id', decoded['user_id'])
        .get()
    ).serialize()

    return data, meta, message, status_code
