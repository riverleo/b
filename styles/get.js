import _ from 'lodash';
import { select } from 'sql-bricks';
import parse, { parseSQLError } from './lib/parse';
import { TABLE, COLUMNS } from './lib/constants';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  let data = [];
  let sql = select().from(TABLE).orderBy(`${COLUMNS.CREATED_AT} DESC`);
  const conn = await getConnection();
  const params = _.get(e, 'queryStringParameters') || {};

  if (!_.isNil(params.active)) {
    sql = sql.where(COLUMNS.ACTIVE, _.toLower(params.active) === 'true');
  }

  if (!_.isNil(params.component)) {
    sql = sql.where(COLUMNS.COMPONENT, params.component);
  }

  let response;

  try {
    data = _.map(await conn.query(sql.toString()), style => parse(style, true));

    response = {
      statusCode: 200,
      body: JSON.stringify({ data }),
    };
  } catch (error) {
    response = {
      statusCode: 400,
      body: JSON.stringify({ error: parseSQLError(error) }),
    };
  } finally {
    conn.end();
  }

  callback(null, response);
};
