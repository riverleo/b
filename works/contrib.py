import sys
import jwt
import json
from datetime import datetime
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
role_types = [
    'author',       # 글
    'reviewer',     # 감수
    'illustrator',  # 그림
]

JWT_SECRET = db.table('secret').where('key', 'JWT').pluck('body')



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


def jwt_encode(user_id):
    encoded = jwt.encode({'user_id': user_id}, JWT_SECRET, algorithm='HS256')

    return encoded.decode('utf8')


def jwt_decode(raw):
    token = raw or ''

    if token.startswith('Bearer'):
        token = raw[7:]

    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except:
        return {}


def new_error(message, code):
    return {
        'code': code,
        'message': message,
    }


def abort(status_code, error):
    return {
        'body': json.dumps({'error': error}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': status_code,
    }


def parse_sql_error(err):
    if hasattr(err, 'previous'):
        code, message = err.previous.args
    else:
        code = None
        message = str(err)

    return new_error(message, code)


def parse(raw):
    contents = []

    if raw.get('contents'):
        contents = json.loads(raw.get('contents'))

    return {
        'id': raw.get('id'),
        'contents': contents,
        'createdAt': raw.get('createdAt'),
    }


def split(raw, separator=','):
    if type(raw) != str:
        return []

    splitted = raw.replace(' ', '').split(separator)

    return splitted if len(splitted) > 0 else None


def can_delete(work_id, user_id):
    role = db.table('workRole').where({
        'workId': work_id,
        'userId': user_id,
        'type': 'author',
    }).first()

    return role is not None


def can_change(work_id, user_id):
    role = db.table('workRole').where({
        'workId': work_id,
        'userId': user_id,
    }).where_in('type', role_types).first()

    return role is not None
