import json
from datetime import datetime
from orator.support.collection import Collection


def converter(o):
    if isinstance(o, Collection):
        return o.serialize()

    if isinstance(o, datetime):
        return o.isoformat() + 'Z'

    if isinstance(o, bytes):
        return o.decode('utf-8')

    return str(o)


def dumps(body):
    return json.dumps(body or {}, default=converter)
