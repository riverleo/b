import get from './methods/get';
import getById from './methods/getById';
import post from './methods/post';

export default (e, ctx, cb) => {
  const body = {};
  const statusCode = 200;

  // 테스트 시에 요청 정보를 응답에 포함하여 보냅니다.
  if (e.requestContext.stage === 'test-invoke-stage') {
    body.e = e;
  }

  if (e.resource === 'GET') {
    if (e.resource === '/users/{id}') {
      body.data = get(e);
    } else if (e.resource === '/users') {
      body.data = getById(e);
    }
  } else if (e.resource === 'POST') {
    body.data = post(e);
  }

  cb(null, { statusCode, body: JSON.stringify(body) });
};
