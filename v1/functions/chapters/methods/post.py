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
    index = body.get('index') or 0
    post_key = body.get('post_key')
    chapter_key = body.get('chapter_key')
    slug = '{}-{}'.format(
        slugify(title),
        create_random_key(length=5, digit_only=True),
    ) if title else None  # noqa: E501

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
        .where('post_key', post_key)
        .where_in('type', ('author', 'assistant'))
        .count()
    ) > 0

    if not is_admin and not is_author:
        return None, None, 'no permission', 401

    query = db.table('chapter').where('key', key)
    chapter = query.first()

    if chapter:
        (
            db.table('chapter')
            .where('id', chapter.get('id'))
            .update({
                'key': key,
                'slug': slug,
                'title': title,
                'index': index,
                'user_id': decoded['user_id'],
                'post_key': post_key,
                'chapter_key': chapter_key,
            })
        )
    else:
        (
            db.table('chapter')
            .insert({
                'key': key,
                'slug': slug,
                'title': title,
                'index': index,
                'user_id': decoded['user_id'],
                'post_key': post_key,
                'chapter_key': chapter_key,
            })
        )

    data = query.first()

    return data, meta, message, status_code
