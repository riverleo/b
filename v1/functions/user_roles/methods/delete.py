import json
from jwt import decode
from datetime import datetime
from .contrib.db import db
from .post import SECRET, TYPES


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

    is_admin = (
        db.table('user_role')
        .where('user_id', decoded['user_id'])
        .where('type', 'admin')
        .where('type', 'active')
        .count()
    ) > 0

    try:
        body = json.loads(e.get('body'))
    except:
        body = {}

    type_ = body.get('type')
    user_id = body.get('user_id')

    # 관리자 또는 본인만 삭제할 수 있다.
    if not is_admin and user_id != decoded['user_id']:
        return None, None, 'no permission', 401

    if type_ not in TYPES:
        return None, None, 'type is invalid or the value is empty', 403

    (
        db.table('user_role')
        .where('user_id', user_id)
        .where('type', type_)
        .delete()
    )

    return data, meta, message, status_code
