import sys
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

types = ['work']


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
