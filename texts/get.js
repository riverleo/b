import _ from 'lodash';
import { select, like } from 'sql-bricks';
import text, { translation } from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const conn = await getConnection();
  const params = _.get(e, 'queryStringParameters') || {};
  const { q, key, lcid, active } = params;

  let data = [];
  let sql = select()
    .from(text.name)
    .join(translation.name, { [translation.textId]: text.id })
    .orderBy(`${text.columns.createdAt} DESC`);

  if (!_.isNil(q)) {
    sql = sql.where(like(translation.columns.body, `%${q}%`));
  }

  if (!_.isNil(key)) {
    sql = sql.where(like(text.columns.key, `%${key}%`));
  }

  if (!_.isNil(lcid)) {
    sql = sql.where(text.columns.lcid, `%${lcid}%`);
  }

  if (!_.isNil(active)) {
    sql = sql.where(text.columns.active, _.toLower(active) === 'true');
  }

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    data = _.map(await conn.query(sql.toString()), style => parse(style, true));

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
