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
    page_key = body.get('page_key')
    index = body.get('index')
    type_ = body.get('type')
    source = json.dumps(body.get('source'))

    post_role = (
        db.table('post_role')
        .where('user_id', decoded['user_id'])
        .where('post_key', post_key)
        .where('status', 'active')
        .first()
    )

    if not post_role:
        return None, None, 'no role', 401

    query = db.table('content').where('key', key)
    content = query.first()

    if content:
        query.update({
            'key': key,
            'post_key': post_key,
            'page_key': page_key,
            'user_id': decoded['user_id'],
            'index': index,
            'type': type_,
            'source': source,
        })
    else:
        db.table('content').insert({
            'key': key,
            'post_key': post_key,
            'page_key': page_key,
            'user_id': decoded['user_id'],
            'index': index,
            'type': type_,
            'source': source,
        })

    data = query.first()

    return data, meta, message, status_code
