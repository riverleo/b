import sys
import jwt
import json
import random
from urllib import parse as urlparse
from urllib.parse import urlencode
from datetime import datetime
from string import digits, ascii_letters
from orator import DatabaseManager
from orator.support.collection import Collection


config = {
    'mysql': {
        'host': '13.125.216.161',
        'user': 'root',
        'driver': 'mysql',
        'password': 'smMX?[JfRxbifapdZJB3oJNT{ho@7KLsGr]XxChZREgoA6r6pL',
        'database': 'wslo',
        'prefix': '',
    },
}

if 'pytest' in sys.modules:
    config['mysql'] = {
        'host': 'localhost',
        'user': 'root',
        'driver': 'mysql',
        'password': 'mysql',
        'database': 'wslo',
        'prefix': '',
    }

db = DatabaseManager(config)


def new_id(length=10, digit_only=False):
    source = digits if digit_only else digits + ascii_letters

    return ''.join(random.choice(source) for _ in range(length))


def converter(o):
    if isinstance(o, Collection):
        return o.serialize()

    if isinstance(o, datetime):
        return o.isoformat() + 'Z'

    if isinstance(o, bytes):
        return o.decode('utf-8')

    return str(o)


def dumps(body):
    return json.dumps(body or {}, default=converter)


def new_error(message, code):
    return {
        'code': code,
        'message': message,
    }


JWT_SECRET = 'F9Tx#tT@Jt873L'


def jwt_encode(user_id):
    encoded = jwt.encode({'user_id': user_id}, JWT_SECRET, algorithm='HS256')

    return encoded.decode('utf8')


def jwt_decode(raw):
    token = raw

    if raw.startswith('Bearer'):
        token = raw[7:]

    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except:
        return {}


def assign_query_params(url, params={}):
    url = 'https://www.workslow.co' if url is None else url
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)
