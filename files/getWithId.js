import _ from 'lodash';
import { select } from 'sql-bricks';
import table from './lib/table';
import abort from './lib/abort';
import parse from './lib/parse';
import parseSQLError from './lib/parse/sqlError';
import parseCacheKey from './lib/parse/cacheKey';
import parseQueryParam from './lib/parse/queryParam';
import getConnection, { getRedis } from './lib/getConnection';

export default async (e, context, callback) => {
  const conn = await getConnection();
  const { id } = _.get(e, 'pathParameters') || {};
  const { name, columns } = table;
  const queryParams = _.get(e, 'queryStringParameters');
  const { b, c, h, q, w } = parseQueryParam(queryParams); // eslint-disable-line object-curly-newline, max-len
  const cacheKey = parseCacheKey(id, _.get(e, queryParams));
  const cacheValue = await getRedis().get(cacheKey);

  if (cacheValue) {
    callback(null, {
      statusCode: 302,
      headers: { Location: cacheValue },
    });

    return;
  }

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    const data = await conn.query(select().from(name).where(columns.id, id).toString());
    const parsed = parse(data[0], true);

    if (_.isEmpty(data)) {
      throw abort(404, 'not found');
    }

    response = {
      body: JSON.stringify({ data: parsed }),
      headers,
      statusCode: 200,
    };
  } catch (error) {
    response = {
      body: JSON.stringify({ error: parseSQLError(error) }),
      headers,
      statusCode: error.statusCode || 400,
    };
  } finally {
    conn.end();
  }

  callback(null, response);
};
