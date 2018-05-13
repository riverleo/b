import json
from props import get, set_props
from contrib import (
    UNIQUE_KEYS,
    db,
    abort,
    password,
    new_error,
    jwt_decode,
    parse_sql_error,
)


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

    props = body.get('props') or {}
    verbose = body.get('verbose')
    user_id = decoded.get('user_id')
    unique_props = {k: v for k, v in props.items() if k in UNIQUE_KEYS}
    custom_props = {k: v for k, v in props.items() if k not in unique_props}

    if db.table('user').where('id', user_id).first() is None:
        return abort(401, new_error('invalid token', 1))

    if 'password' in custom_props:
        custom_props['password'] = password(custom_props['password'])

    try:
        set_props(user_id, props=unique_props, unique=True)
        set_props(user_id, props=custom_props)
    except Exception as e:
        return abort(400, parse_sql_error(e))

    return {
        'body': json.dumps({
            'data': get(
                user_id,
                keys=props.keys(),
                verbose=verbose,
            ),
        }),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
