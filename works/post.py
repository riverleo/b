import json
from contrib import db, dumps, parse, abort, parse_sql_error


def handler(event, context):
    try:
        body = json.loads(event.get('body'))
    except:
        body = {}

    id_ = body.get('id')
    contents = body.get('contents')

    work = db.table('work').where('id', id_).first()

    try:
        if work is None:
            db.table('work').insert({'id': id_, 'contents': json.dumps(contents)})
            work = db.table('work').where('id', id_).first()
        else:
            db.table('work').where('id', id_).update({'contents': json.dumps(contents)})
    except Exception as e:
        return abort(400, parse_sql_error(e))

    return {
        'body': dumps({'data': parse(work)}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 201,
    }
