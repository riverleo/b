import sys
import jwt
import json
from datetime import datetime
from contrib import db, abort, new_error, jwt_decode, can_delete


def handler(event, context):
    headers = event.get('headers') or {}
    user_id = jwt_decode(headers.get('Authorization')).get('user_id')
    path_params = event.get('pathParameters') or {}
    work_id = path_params.get('id')

    work = db.table('work').where({'id': work_id}).first()

    if work is None:
        return abort(404, new_error('invalid id', 1))

    if not can_delete(work_id, user_id):
        return abort(404, new_error('no permissions', 2))

    db.table('work').where({'id': work_id}).update({
        'deletedAt': datetime.now(),
    })

    return {
        'body': json.dumps({'data': True}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
