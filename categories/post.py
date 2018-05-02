import json
from contrib import db, dumps, types, abort, new_error


def handler(event, context):
    try:
        body = json.loads(event.get('body'))
    except:
        body = {}

    categorizable_id = body.get('categorizableId')
    categorizable_type = body.get('categorizableType')

    if categorizable_type is not None and categorizable_type not in types:
        return abort(403, new_error('invalid categorizable type', 1))

    category_ids = []

    for key in body.get('keys') or []:
        category_id = db.table('category').where('key', key).pluck('id')

        if category_id is None:
            category_id = db.table('category').insert_get_id({'key': key})

        category_ids.append(category_id)

    if categorizable_id is not None and categorizable_type is not None:
        db.table('categoryMap').where({
            'categorizableId': categorizable_id,
            'categorizableType': categorizable_type,
        }).delete()

        for category_id in category_ids:
            db.table('categoryMap').insert({
                'categoryId': category_id,
                'categorizableId': categorizable_id,
                'categorizableType': categorizable_type,
            })

    return {
        'body': dumps({'data': True}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 201,
    }
