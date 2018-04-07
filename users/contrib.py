import jwt
import sys
import json
import random
import hashlib
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


UNIQUE_KEYS = ('username', 'email')


def new_id(length=10, digit_only=False):
    source = digits if digit_only else digits + ascii_letters

    return ''.join(random.choice(source) for _ in range(length))


def password(raw_password):
    def h(raw, salt):
        sha = hashlib.sha512()

        sha.update(salt.encode('utf-8'))
        sha.update(raw.encode('utf-8'))

        return str(sha.hexdigest())

    s1 = '7pA=sGT9=cM8n3'
    s2 = 'r[EQU)64LT72zA'
    s3 = 'rWpNn>*22MWB44'

    return h(h(h(raw_password, s1), s2), s3)


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


def split(s, delimeter=','):
    if type(s) != str or s is '' or s is None:
        return []

    return s.split(delimeter)


def lower(s):
    if type(s) != str or s is '' or s is None:
        return ''

    return s.lower()


def boolean(s):
    return lower(s) == 'true'


def new_error(message, code):
    return {
        'code': code,
        'message': message,
    }


def parse_sql_error(err):
    if hasattr(err, 'previous'):
        code, message = err.previous.args
    else:
        code = None
        message = str(err)

    return new_error(message, code)


def abort(status_code, error):
    return {
        'body': json.dumps({'error': error}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': status_code,
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
