import os
import json
from jwt import decode
from .contrib.db import db
from .contrib.utils import create_random_key

SECRET = os.environ.get('SECRET') or 'SECRET'


def delete(e={}):
    data = None
    meta = None
    message = None
    status_code = 200

    try:
        jwt = e.get('headers', {}).get('Authorization')[4:]
        decoded = decode(jwt, SECRET, algorithm='HS256')
    except:
        return None, None, 'invalid auth token', 401

    try:
        body = json.loads(e.get('body'))
    except:
        body = {}

    key = body.get('key')
    page_id = (e.get('pathParameters') or {}).get('id')
    page = db.table('page').or_where('id', page_id).or_where('key', key).first()
    post = db.table('post').where('key', page['post_key']).first()

    if not page:
        return None, None, 'key are invalid or the value is empty', 403

    is_admin = (
        db.table('user_role')
        .where('user_id', decoded['user_id'])
        .where('type', 'admin')
        .where('status', 'active')
        .count()
    ) > 0
    is_author = (
        db.table('post_role')
        .where('status', 'active')
        .where('user_id', decoded['user_id'])
        .where('post_key', post['key'])
        .where_in('type', ('author', 'assistant'))
        .count()
    ) > 0

    if not is_admin and not is_author:
        return None, None, 'no permission', 401

    db.table('page').where('key', key).delete()

    return data, meta, message, status_code
