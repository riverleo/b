from contrib import db

unique_fields = [
]

def parse(prop, verbose):
    if not verbose:
        return prop.get('value')

    return {
        'value': prop.get('value'),
        'unique': bool(prop.get('unique')),
        'active': bool(prop.get('active')),
    }


def get_props(user_id, keys=[], active=True, verbose=False):
    if keys is None or len(keys) == 0:
        return {}

    query = (
        db.table('userProperty')
        .where('userId', user_id)
        .where_in('key', keys)
        .order_by('createdAt', 'DESC')
    )

    if active is not None:
        query = query.where('active', active)

    props = {}
    all_props = query.get()

    for key in keys:
        if key in props:
            continue

        key_props = list(filter(lambda p: p.get('key') == key, all_props))

        if active:
            try:
                props[key] = parse(key_props[0], verbose)
            except IndexError:
                props[key] = None
        else:
            props[key] = list(map(lambda p: parse(p, verbose), key_props))

    return props


def set_props(user_id, props={}, unique=None):
    (   # 기존 값들을 무효화
        db.table('userProperty')
        .where('userId', user_id)
        .where_in('key', list(props.keys()))
        .update(unique=None, active=None)
    )

    for key, value in props.items():
        db.table('userProperty').insert({
            'userId': user_id,
            'key': key,
            'value': value,
            'active': True,
            'unique': unique,
        })

    return props


def get(user_id, keys=[], active=True, verbose=False):
    props = get_props(
        user_id,
        keys=keys,
        active=active,
        verbose=verbose,
    )

    return {
        'id': user_id,
        'props': props,
    }
