import os
import jwt
import json
from .contrib.db import db
from .contrib.action import log
from validate_email import validate_email as is_valid

SECRET = os.environ.get('SECRET') or 'SECRET'


def post(e={}, **kwargs):
    data = None
    meta = None
    message = None
    status_code = 201

    try:
        body = json.loads(e.get('body'))
    except:
        body = {}

    id = body.get('id')
    email = body.get('email') or ''
    raw_password = body.get('password') or ''

    fields = (
        'id', 'name', 'email', 'password',
        'lang', 'country', 'created_at',
    )

    if not is_valid(email) or len(raw_password) < 4:
        return None, None, 'params are invalid or the value is empty', 403

    data = db.table('user').select(*fields).where('email', email).first()
    body['password'] = (
        jwt.encode({'password': raw_password}, SECRET, algorithm='HS256')
        .decode('utf-8')
    )
    e['body'] = body

    if not data:
        id = db.table('user').insert_get_id(body)

        data = db.table('user').select(*fields).where('id', id).first()
        data['is_new'] = True

        log(
            e,
            'SIGN_UP',
            user_id=data['id'],
            description='sign up with email and password.',
        )
    else:
        if body['password'] != data['password']:
            log(
                e,
                'LOGIN_FAILURE',
                user_id=data['id'],
                description='fail to login because of invalid password.',
            )

            return None, None, 'params are invalid or the value is empty', 403

        log(
            e,
            'LOGIN',
            user_id=data['id'],
            description='login with email and password',
        )
        data['is_new'] = False

    del data['password']
    data['jwt'] = (
        jwt.encode({'user_id': data['id']}, SECRET, algorithm='HS256')
        .decode('utf-8')
    )

    return data, meta, message, status_code
