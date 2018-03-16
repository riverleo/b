import _ from 'lodash';
import { select } from 'sql-bricks';
import locale from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const conn = await getConnection();
  const params = _.get(e, 'queryStringParameters') || {};
  const { name, columns } = locale;
  const { country, language, active } = params;

  let data = [];
  let sql = select().from(name).orderBy(`${columns.createdAt} DESC`);

  if (!_.isNil(country)) {
    sql = sql.where(columns.country, country);
  }

  if (!_.isNil(language)) {
    sql = sql.where(columns.language, language);
  }

  if (!_.isNil(active)) {
    sql = sql.where(columns.active, _.toLower(active) === 'true');
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
