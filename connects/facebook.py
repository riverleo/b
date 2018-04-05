import json
from requests import get
from props import set_connection


FB_APP_ID = '691683050955452'
FB_APP_SECRET = '20d0680cf03fc37ca98aefb722fa8f6e'


def handler(event, context):
    headers = event.get('headers') or {}
    query_params = event.get('queryStringParameters') or {}

    code = query_params.get('code')
    referer = query_params.get('referer') or headers.get('Referer')
    redirect_uri = 'https://api.wslo.co/connects/facebook'

    if code is None:
        location = '{}?client_id={}&redirect_uri={}&state={}&scope={}'.format(
            'https://www.facebook.com/v2.12/dialog/oauth',
            FB_APP_ID,
            redirect_uri,
            json.dumps({'referer': referer}),
            'email',
        )
    else:
        if 'state' in query_params:
            state = json.loads(query_params['state'])
        else:
            state = {}

        token_uri = 'https://graph.facebook.com/v2.12/oauth/access_token'
        token_res = get(token_uri, params={
            'code': code,
            'client_id': FB_APP_ID,
            'client_secret': FB_APP_SECRET,
            'redirect_uri': redirect_uri,
        }).json()

        access_token = token_res.get('access_token')

        data = get('https://graph.facebook.com/v2.12/me', params={
            'fields': 'id,email,name',
            'locale': headers.get('CloudFront-Viewer-Country'),
            'access_token': access_token,
        }).json()

        connection, location = set_connection(
            'facebook',
            data.get('id'),
            access_token,
            state.get('referer'),
            props={
                'candidateName': data.get('name'),
                'candidateEmail': data.get('email'),
            }
        )

    return {
        'statusCode': 302,
        'headers': {
            'Location': location,
        },
    }
