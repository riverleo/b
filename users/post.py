import json
from props import get, set_props
from contrib import (
    UNIQUE_KEYS,
    db,
    abort,
    dumps,
    new_id,
    password,
    parse_sql_error,
)


def handler(event, context):
    user_id = new_id()

    while db.table('user').where({'id': user_id}).first():
        user_id = new_id()

    try:
        body = json.loads(event.get('body'))
    except:
        body = {}

    props = body.get('props') or {}
    verbose = body.get('verbose')
    unique_props = {k: v for k, v in props.items() if k in UNIQUE_KEYS}
    custom_props = {k: v for k, v in props.items() if k not in unique_props}

    if 'password' in custom_props:
        custom_props['password'] = password(custom_props['password'])

    try:
        set_props(user_id, props=unique_props, unique=True)
        set_props(user_id, props=custom_props)
        db.table('user').insert(id=user_id)
    except Exception as e:
        return abort(400, parse_sql_error(e))

    return {
        'body': dumps({
            'data': get(
                user_id,
                keys=[k for k in props.keys() if k != 'password'],
                verbose=verbose,
                with_ssid=True,
            )
        }),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 201,
    }
