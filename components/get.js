import _ from 'lodash';
import { select, like } from 'sql-bricks';
import component from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  let data = [];
  let sql = select().from(component.name).orderBy(`${component.columns.createdAt} DESC`);
  const conn = await getConnection();
  const params = _.get(e, 'queryStringParameters') || {};
  const { columns } = component;
  const { q, key } = params;

  if (!_.isNil(q)) {
    sql = sql.where(like(columns.key, `%${key}%`));
  }

  if (!_.isNil(key)) {
    sql = sql.where(columns.key, key);
  }

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    data = _.map(await conn.query(sql.toString()), s => parse(s, true));

    response = {
      body: JSON.stringify({ data }),
      headers,
      statusCode: 200,
    };
  } catch (error) {
    response = {
      body: JSON.stringify({ error: parseSQLError(error) }),
      headers,
      statusCode: 400,
    };
  } finally {
    conn.end();
  }

  callback(null, response);
};
