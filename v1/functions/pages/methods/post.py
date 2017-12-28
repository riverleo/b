import os
import json
from jwt import decode
from slugify import slugify
from .contrib.db import db
from .contrib.utils import create_random_key

SECRET = os.environ.get('SECRET') or 'SECRET'


def post(e={}):
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

    key = body.get('key') or create_random_key(length=10)
    post_key = body.get('post_key')
    chapter_key = body.get('chapter_key')
    status = body.get('status') or 'draft'

    post_role = (
        db.table('post_role')
        .where('user_id', decoded['user_id'])
        .where('post_key', post_key)
        .where('status', 'active')
        .first()
    )

    if not post_role:
        return None, None, 'no role', 401

    query = db.table('page').where('key', key)
    page = query.first()

    if page:
        query.update({
            'key': key,
            'post_key': post_key,
            'chapter_key': chapter_key,
            'user_id': decoded['user_id'],
        })
    else:
        db.table('page').insert({
            'key': key,
            'post_key': post_key,
            'chapter_key': chapter_key,
            'user_id': decoded['user_id'],
        })

    data = query.first()

    return data, meta, message, status_code
