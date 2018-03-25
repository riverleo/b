import _ from 'lodash';
import { select, in as $in, like } from 'sql-bricks';
import table from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const conn = await getConnection();
  const params = _.get(e, 'queryStringParameters') || {};
  const { message, translation } = table;
  const {
    q,
    key,
    lcid,
  } = params;
  const columns = [
    message.columns.id,
    message.columns.key,
    translation.columns.body,
    translation.columns.lcid,
  ];

  let data = [];
  let sql = select(columns)
    .from(message.name)
    .leftJoin(translation.name, { [translation.columns.messageId]: message.columns.id })
    .orderBy(`${message.columns.createdAt} DESC`);

  if (!_.isNil(q)) {
    const inSQL = select(message.columns.id)
      .from(message.name)
      .join(translation.name, { [translation.columns.messageId]: message.columns.id })
      .where(like(translation.columns.body, `%${q}%`))
      .groupBy(message.columns.id)
      .orderBy(`${message.columns.createdAt} DESC`);

    sql = select(columns)
      .from(message.name)
      .join(translation.name, { [translation.columns.messageId]: message.columns.id })
      .where($in(message.columns.id, inSQL))
      .orderBy(`${message.columns.createdAt} DESC`);
  }

  if (!_.isNil(key)) {
    sql = sql.where(like(message.columns.key, `%${key}%`));
  }

  if (!_.isNil(lcid)) {
    sql = sql.where(translation.columns.lcid, lcid);
  }

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    const grouped = _.groupBy(await conn.query(sql.toString()), 'id');
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
