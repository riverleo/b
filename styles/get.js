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
  const { active, component, groupBy } = params;

  if (!_.isNil(active)) {
    sql = sql.where(COLUMNS.ACTIVE, _.toLower(active) === 'true');
  }

  if (!_.isNil(component)) {
    sql = sql.where(COLUMNS.COMPONENT, component);
  }

  if (!_.isNil(groupBy) && _.includes(_.values(COLUMNS), groupBy)) {
    sql = sql.groupBy(groupBy);
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
