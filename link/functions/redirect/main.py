import os
import sys
sys.path.insert(0, 'lib')  # Make `./lib` directory to python packages.

from orator import DatabaseManager  # noqa: E402

db = DatabaseManager({
    'default': 'mysql',
    'mysql': {
        'driver': 'mysql',
        'host': os.environ.get('MySQL_HOST') or 'localhost',
        'database': os.environ.get('MySQL_DATABASE') or 'zeitstories',
        'user': os.environ.get('MySQL_USER') or 'root',
        'password': os.environ.get('MySQL_PASSWORD') or 'mysql',
        'use_qmark': True,
    }
})


def handle(e, context):
    body = {}
    status_code = 301
    path_params = e.get('pathParameters') or {}

    # Sending request data and context info in API Gateway tests.
    if e.get('requestContext', {}).get('stage') == 'test-invoke-stage':
        body['event'] = e
        body['context'] = {k: v for k, v in context.__dict__.items() if type(v) in [int, float, bool, str, list, dict]}  # noqa: E501

    link = (
        db.table('link')
        .where('key', path_params.get('key'))
        .first()
    )

    return {
        'statusCode': status_code,
        'body': None,
        'headers': {
            'Location': link['href'] if link else 'https://www.workslow.co',
        },
    }
