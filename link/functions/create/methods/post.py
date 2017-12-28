import json
from .contrib.db import db
from .contrib.utils import create_random_key


def post(e={}):
    data = None
    meta = None
    message = None
    status_code = 201

    try:
        body = json.loads(e.get('body'))
    except:
        body = {}

    href = body.get('href')

    if not href:
        status_code = 403
        message = '`href` is invalid'

        return data, meta, message, status_code

    key = create_random_key(length=10)
    query = db.table('link').where('href', href)
    link = query.first()

    if not link:
        db.table('link').insert(href=href, key=key)
        link = query.first()

    data = link
    data['link'] = 'scdc.co/{}'.format(link['key'])

    return data, meta, message, status_code
