from jwt import decode
from datetime import datetime
from .post import SECRET
from .contrib.db import db


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

    params = e.get('pathParameters') or {}
    id_ = params.get('id')
    query = (
        db.table('post')
        .or_where('id', id_)
        .or_where('key', str(id_))
        .or_where('slug', id_)
    )

    post = query.first()
    role = (
        db.table('post_role')
        .where('user_id', decoded['user_id'])
        .where('post_key', post['key'])
        .where('status', 'active')
        .first()
    )

    if not post:
        return None, None, 'not found', 404

    if not role:
        return None, None, 'no permission', 401

    query.update({'deleted_at': datetime.now()})

    return data, meta, message, status_code
