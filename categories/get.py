from contrib import db, dumps


def handler(event, context):
    return {
        'body': dumps({
            'data': db.table('category').lists('key'),
        }),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
