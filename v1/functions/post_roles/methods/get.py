import json
from .contrib.db import db


def get(e={}):
    data = None
    meta = None
    message = None
    status_code = 200

    body = e.get('queryStringParameters') or {}
    secret = body.get('secret')

    if not secret:
        status_code = 403
        message = 'secret is invalid'

        return data, meta, message, status_code

    fields = (
        'post_role.id',
        'post_role.user_id',
        'post_role.grantor_id',
        'post_role.type',
        'post_role.post_key',
        'post_role.secret',
        'post_role.status',
        'post_role.created_at',
        'post_role.updated_at',
    )

    data = (
        db.table('post_role')
        .select(*fields)
        .where('secret', secret)
        .get()
    )

    return data, meta, message, status_code
