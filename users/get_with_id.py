import json
from props import get, set_props
from contrib import db, split, boolean


def handler(event, context):
    headers = event.get('headers') or {}
    authorization = headers.get('Authorization')
    query_params = event.get('queryStringParameters') or {}
    path_params = event.get('pathParameters')

    user_id = path_params.get('id')
    keys = split(query_params.get('props'))
    verbose = boolean(query_params.get('verbose'))

    data = get(
        user_id=user_id,
        keys=keys,
        verbose=verbose,
    )

    return {
        'body': json.dumps({'data': data}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
