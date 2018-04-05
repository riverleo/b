import json
import requests
import facebook
from contrib import new_error


def handler(event, context):
    path_params = event.get('pathParameters') or {}
    provider = path_params.get('provider')

    if provider == 'facebook':
        return facebook.handler(event, context)

    return {
        'statusCode': 403,
        'body': json.dumps(new_error('invalid provider ({})'.format(provider), 1)),
    }
