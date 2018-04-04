import json
from contrib import db


def handler(event, context):
    try:
        body = json.loads(event.get('body'))
    except:
        body = {}

    data = {}
    props = body.get('props') or {}
    unique_props = {k: v for k, v in props.items() if k in ['name', 'email']}

    for k, v in unique_props.items():
        prop = db.table('userProperty').where({
            'key': k,
            'value': v,
            'unique': True,
        }).first()

        data[k] = {
            'value': v,
            'exists': prop is not None,
        }

    response = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'data': data}),
    }

    return response
