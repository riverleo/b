import os
import boto3
from jwt import decode
from uuid import uuid4
from io import BytesIO
from base64 import b64encode, b64decode
from os.path import splitext
from .contrib.db import db
from .contrib.image import get_image_size, UnknownImageFormat

s3 = boto3.Session(
    aws_access_key_id=os.environ.get('ACCESS_KEY_ID', 'AKIAIN3HLHS26Z4CLVUA'),
    aws_secret_access_key=os.environ.get('SECRET_ACCESS_KEY', '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'),  # noqa: E501
).resource('s3')
SECRET = os.environ.get('SECRET') or 'SECRET'


def post(e={}):
    data = None
    meta = None
    message = None
    status_code = 201

    try:
        jwt = e.get('headers', {}).get('Authorization')[4:]
        decoded = decode(jwt, SECRET, algorithm='HS256')
    except:
        decoded = {}

    body = e.get('body')
    is_base64 = e.get('isBase64Encoded')
    params = e.get('queryStringParameters') or {}
    headers = e.get('headers') or {}
    name = params.get('name')

    if name is None:
        status_code = 403
        message = 'name is required'

        return data, meta, message, status_code

    user_id = decoded.get('user_id')
    attachable_id = params.get('attachable_id')
    attachable_type = params.get('attachable_type')
    key = '{}{}'.format(str(uuid4()), splitext(name)[1])
    type_ = headers.get('Content-Type') or headers.get('content-type')
    bucket = 'static.scdc.co'
    encoded = body.encode('utf-8')
    b64body = b64decode(encoded) if is_base64 else encoded

    if not os.environ.get('PYTEST_CURRENT_TEST'):
        s3.Bucket(bucket).put_object(
            Key='origin/{}'.format(key),
            Body=b64body,
            ContentType=type_,
            ACL='public-read'
        )

    size = (len(encoded) * 3) / 4 if is_base64 else len(encoded)

    try:
        width, height = get_image_size(BytesIO(b64body), size)
    except:
        width = 0
        height = 0

    file_id = db.table('file').insert_get_id({
        'key': key,
        'name': name,
        'type': type_,
        'size': size,
        'width': width,
        'height': height,
        'bucket': bucket,
        'user_id': user_id,
        'attachable_id': attachable_id,
        'attachable_type': attachable_type,
    })

    data = db.table('file').where('id', file_id).first()
    data['url'] = 'https://{}/{}'.format(bucket, key)


    return data, meta, message, status_code
