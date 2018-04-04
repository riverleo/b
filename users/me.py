import json
from props import get
from contrib import db, abort, new_error, jwt_decode


def handler(event, context):
    headers = event.get('headers') or {}
    authorization = headers.get('Authorization')

    try:
        body = json.loads(event.get('body'))
    except:
        body = {}

    try:
        decoded = jwt_decode(authorization)
    except:
        decoded = {}

    keys = body.get('props')
    verbose = body.get('verbose')
    user_id = decoded.get('user_id')

    if db.table('user').where('id', user_id).first() is None:
        return abort(400, {'error': new_error('invalid token', 1)})

    return {
        'body': json.dumps({'data': get(user_id, keys=keys, verbose=verbose)}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
