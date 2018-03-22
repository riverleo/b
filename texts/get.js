import _ from 'lodash';
import { select, in as $in, like } from 'sql-bricks';
import table from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const conn = await getConnection();
  const params = _.get(e, 'queryStringParameters') || {};
  const { text, translation } = table;
  const {
    q,
    key,
    lcid,
  } = params;

  let data = [];
  let sql = select()
    .from(text.name)
    .join(translation.name, { [translation.columns.textId]: text.columns.id })
    .orderBy(`${text.columns.createdAt} DESC`);

  if (!_.isNil(q)) {
    sql = sql.select(text.columns.id).where(like(translation.columns.body, `%${q}%`)).groupBy(text.columns.id);
    sql = select()
      .from(text.name)
      .join(translation.name, { [translation.columns.textId]: text.columns.id })
      .where($in(text.columns.id, sql))
      .orderBy(`${text.columns.createdAt} DESC`);
  }

  if (!_.isNil(key)) {
    sql = sql.where(like(text.columns.key, `%${key}%`));
  }

  if (!_.isNil(lcid)) {
    sql = sql.where(translation.columns.lcid, lcid);
  }

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    const grouped = _.groupBy(await conn.query(sql.toString()), 'textId');
    data = _.map(_.values(grouped), t => parse(t, true));

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
