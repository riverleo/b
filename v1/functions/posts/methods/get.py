from .contrib.db import db


def get(e={}, **kwargs):
    data = []
    meta = {}
    message = None
    status_code = 200

    params = e.get('queryStringParameters') or {}
    status = params.get('status')
    user_id = params.get('user_id')

    try:
        per = min(int(params.get('per', 20)), 20)  # default 20
        page = max(int(params.get('page', 1)), 1)  # default 1
    except:
        per = 20
        page = 1
        text = 'invalid pagination params (per: {}, page: {})'
        message = text.format(params.get('per'), params.get('page'))

    fields = (
        'post.id',
        'post.key',
        'post.title',
        'post.slug',
        'post.created_at',
        'post.updated_at',
    )
    query = (
        db.table('post')
        .select(*fields)
        .where_null('post.deleted_at')
    )

    if status:
        query = query.where('post.status', status)

    if user_id:
        query = query.join('post_role', 'post.key', '=', 'post_role.post_key')
        query = query.where('post_role.user_id', user_id)

    results = query.paginate(per, page)

    for result in results.serialize():
        data.append(result)

    meta['total'] = results.total
    meta['next_page'] = results.next_page
    meta['last_page'] = results.last_page
    meta['current_page'] = results.current_page
    meta['previous_page'] = results.previous_page
    meta['has_more_page'] = results.has_more_pages()

    return data, meta, message, status_code
