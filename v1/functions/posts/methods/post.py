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
    title = body.get('title')
    status = body.get('status')
    slug = '{}-{}'.format(
        slugify(title),
        create_random_key(length=5, digit_only=True),
    ) if title else None  # noqa: E501

    if type(title) == str and len(title) > 180:
        return None, None, 'title is exceeds 180 characters', 403

    if type(key) != str or len(key) > 10:
        return None, None, 'key is not string or exceeds 10 characters', 403

    query = db.table('post').where('key', key)
    post = query.first()

    if post:
        query.update({
            'slug': post['slug'] if post['slug'] else slug,
            'title': title,
            'status': status or post['status'],
        })
    else:
        post_id = db.table('post').insert_get_id({
            'key': key,
            'slug': slug,
            'title': title,
            'status': status or 'draft',
        })
        db.table('post_role').insert(
            user_id=decoded['user_id'],
            post_key=key,
            type='author',
            status='active',
        )

    data = query.first()

    return data, meta, message, status_code
