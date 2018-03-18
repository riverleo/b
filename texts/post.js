import _ from 'lodash';
import { select, insert } from 'sql-bricks';
import text, { translation } from './lib/constants';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const picked = _.pick(JSON.parse(e.body), [
    text.columns.key,
    translation.columns.lcid,
    translation.columns.body,
  ]);
  const sql = insert(TABLE, parse(picked, true));
  const conn = await getConnection();

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    const { insertId } = await conn.query(sql.toString());
    const data = await conn.query(select().from(TABLE).where({ id: insertId }).toString());

    response = {
      body: JSON.stringify({ data: parse(data[0], true) }),
      headers,
      statusCode: 201,
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
