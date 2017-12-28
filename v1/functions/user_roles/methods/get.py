from jwt import decode
from .contrib.db import db
from .post import SECRET


def get(e={}, **kwargs):
    data = []
    meta = {}
    message = None
    status_code = 200

    try:
        jwt = e.get('headers', {}).get('Authorization')[4:]
        decoded = decode(jwt, SECRET, algorithm='HS256')
    except:
        return None, None, 'invalid auth token', 401

    params = e.get('queryStringParameters') or {}
    status = params.get('status')
    secret = params.get('secret')

    try:
        per = min(int(params.get('per', 20)), 20)  # default 20
        page = max(int(params.get('page', 1)), 1)  # default 1
    except:
        per = 20
        page = 1
        text = 'invalid pagination params (per: {}, page: {})'
        message = text.format(params.get('per'), params.get('page'))

    fields = (
        'user_role.id',
        'user_role.type',
        'user_role.user_id',
        'user_role.grantor_id',
        'user_role.secret',
        'user_role.status',
        'user_role.created_at',
        'user_role.updated_at',
        'user.id',
        'user.name',
        'grantor.id',
        'grantor.name',
    )

    query = (
        db.table('user_role')
        .left_join('user', 'user_role.user_id', '=', 'user.id')
        .left_join('user as grantor', 'user_role.grantor_id', '=', 'grantor.id')
        .select(*fields)
    )

    if secret:
        query = query.where('secret', secret)
    else:
        query = query.where('grantor_id', decoded['user_id'])

    if status:
        query = query.where('user_role.status', status)

    results = query.paginate(per, page)

    for result in results.serialize():
        if result['grantor_id']:
            result['grantor'] = {
                'id': result['grantor.id'],
                'name': result['grantor.name'],
            }
        else:
            result['grantor'] = None

        if result['user.id']:
            result['user'] = {
                'id': result['user.id'],
                'name': result['name'],
            }
        else:
            result['user'] = None

        del result['user.id']
        del result['name']
        del result['grantor.id']
        del result['grantor.name']

        data.append(result)

    meta['total'] = results.total
    meta['next_page'] = results.next_page
    meta['last_page'] = results.last_page
    meta['current_page'] = results.current_page
    meta['previous_page'] = results.previous_page
    meta['has_more_page'] = results.has_more_pages()

    return data, meta, message, status_code
