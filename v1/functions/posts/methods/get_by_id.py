import re
import json
from .contrib.db import db


def get_by_id(e={}):
    data = None
    meta = None
    message = None
    status_code = 200

    params = e.get('pathParameters') or {}
    id_ = str(params.get('id'))

    fields = (
        'post.id',
        'post.key',
        'post.title',
        'post.slug',
        'post.status',
        'post.created_at',
        'post.updated_at',
    )

    r = re.compile(r'^[0-9]+$')
    query = db.table('post').select(*fields)

    if r.match(id_):
        query = query.where('id', id_)
    else:
        query = query.or_where('key', id_).or_where('slug', id_)

    data = query.first()

    if not data:
        return None, None, None, 404

    data['pages'] = db.table('page').where('post_key', data['key']).get()
    data['chapters'] = db.table('chapter').where('post_key', data['key']).order_by('index', 'asc').get()
    contents = db.table('content').where('post_key', data['key']).order_by('index', 'asc').get()

    for content in contents:
        content['source'] = json.loads(content['source'])

    data['contents'] = contents
    data['roles'] = list(
        db.table('post_role')
        .select(
            'post_role.id',
            'post_role.user_id',
            'post_role.post_key',
            'post_role.type',
            'user.name as username',
        )
        .join('user', 'user.id', '=', 'post_role.user_id')
        .where('post_key', data['key'])
        .where('status', 'active')
        .get()
    )

    return data, meta, message, status_code
