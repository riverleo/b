from contrib import db, parse, dumps


def handler(event, context):
    path_params = event.get('pathParameters')
    work_id = path_params.get('id')

    work = db.table('work').where('id', work_id).first()

    if work is None:
        return abort(404, 'not found')

    return {
        'body': dumps({'data': parse(work)}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
