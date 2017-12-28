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
        text = 'invalid pagination params. (per: {}, page: {})'
        message = text.format(params.get('per'), params.get('page'))

    fields = ('user.id', 'user.name', 'user.lang', 'user.country')
    query = (
        db.table('user')
        .select(*fields)
    )

    results = query.paginate(per, page).serialize()

    for result in results:
        data.append(result)

    return data, meta, message, status_code
