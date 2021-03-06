from contrib import db, new_id, assign_query_params, jwt_encode


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


def set_connection(provider, provider_id, access_token, referer, props={}):
    connection = (
        db.table('userConnection')
        .where({
            'provider': provider,
            'providerId': provider_id,
        }).first()
    )

    if connection:
        created = False
        user_id = connection.get('userId')
        (
            db.table('userConnection')
            .where('providerId', provider_id)
            .update({'token': access_token})
        )
    else:
        created = True
        user_id = new_id()

        conn_id = db.table('userConnection').insert_get_id({
            'userId': user_id,
            'provider': provider,
            'providerId': provider_id,
            'token': access_token,
        })

        db.table('user').insert(id=user_id)
        set_props(user_id, props=props)

        connection = db.table('userConnection').where('id', conn_id).first()

    location = assign_query_params(referer, {
        'ssid': jwt_encode(connection.get('userId')),
        'created': int(created),
    })

    return connection, location
