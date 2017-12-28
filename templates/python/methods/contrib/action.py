from .db import db
from .json import dumps

def log(e, type_, user_id=None, actable_id=None, actable_type=None, description=None):
    json = {'event': e}

    if description:
        json['description'] = description

    db.table('action').insert({
        'user_id': user_id,
        'actable_id': actable_id,
        'actable_type': actable_type,
        'type': type_,
        'json': dumps(json),
    })
