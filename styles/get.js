import _ from 'lodash';
import { select } from 'sql-bricks';
import style from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  let data = [];
  let sql = select().from(style.name).orderBy(`${style.columns.createdAt} DESC`);
  const conn = await getConnection();
  const params = _.get(e, 'queryStringParameters') || {};
  const { columns } = style;
  const { active, component, groupBy } = params;

  if (!_.isNil(active)) {
    sql = sql.where(columns.active, _.toLower(active) === 'true');
  }

  if (!_.isNil(component)) {
    sql = sql.where(columns.component, component);
  }

  if (!_.isNil(groupBy) && _.includes(_.values(style.columns), groupBy)) {
    sql = sql.groupBy(groupBy);
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
