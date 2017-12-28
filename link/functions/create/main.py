import sys
sys.path.insert(0, 'lib')  # Make `./lib` directory to python packages.

from methods.post import post  # noqa: E402
from methods.contrib.json import dumps  # noqa: E402


def handle(e, context):
    body = {}
    status_code = 403
    path_params = e.get('pathParameters') or {}

    # Sending request data and context info in API Gateway tests.
    if e.get('requestContext', {}).get('stage') == 'test-invoke-stage':
        body['event'] = e
        body['context'] = {k: v for k, v in context.__dict__.items() if type(v) in [int, float, bool, str, list, dict]}  # noqa: E501

    if e.get('httpMethod') == 'POST':
        body['data'], body['meta'], body['message'], status_code = post(e=e)
    elif e.get('httpMethod') == 'GET':
        return {
            'statusCode': 301,
            'body': None,
            'headers': {
                'Location': 'https://www.wearescdc.com',
            },
        }
    elif e.get('httpMethod') == 'OPTIONS':
        status_code = 200

    return {
        'statusCode': status_code,
        'body': dumps({k: v for k, v in body.items() if v is not None}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT',  # noqa: E501
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',  # noqa: E501
        },
    }
