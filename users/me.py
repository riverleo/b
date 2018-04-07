import json
from props import get, get_props
from contrib import db, abort, new_error, jwt_decode, split, boolean, password


def handler(event, context):
    headers = event.get('headers') or {}
    query_params = event.get('queryStringParameters') or {}
    authorization = headers.get('Authorization')

    try:
        body = json.loads(event.get('body'))
    except:
        body = {}

    try:
        decoded = jwt_decode(authorization)
    except:
        decoded = {}

    keys = body.get('props') or split(query_params.get('props'))
    verbose = body.get('verbose') or boolean(query_params.get('verbose'))
    user_id = decoded.get('user_id')

    email = body.get('email') or query_params.get('email')
    username = body.get('username') or query_params.get('username')
    raw_password = body.get('password') or query_params.get('password')

    if raw_password is not None:
        credential = (
            db.table('userProperty')
            .or_where(
                db.query().where({
                    'key': 'email',
                    'value': email,
                    'active': True,
                })
            )
            .or_where(
                db.query().where({
                    'key': 'username',
                    'value': username,
                    'active': True,
                })
            )
            .first()
        )

        if credential is None:
            return abort(400, new_error('invalid credentials', 2))

        user_id = credential.get('userId')
        user_password = get_props(user_id, keys=['password'])['password']

        if password(raw_password) != user_password:
            return abort(400, new_error('invalid credentials', 2))

    if db.table('user').where('id', user_id).first() is None:
        return abort(400, new_error('invalid token', 1))

    data = get(user_id, keys=keys, verbose=verbose, with_ssid=True)

    return {
        'body': json.dumps({'data': data}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
