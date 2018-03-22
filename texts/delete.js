import { delete as del } from 'sql-bricks';
import table from './lib/table';
import { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const { id } = e.pathParameters;
  const { text, translation } = table;
  const conn = await getConnection();

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    await conn.query(del(text.name).where({ id }).toString());
    await conn.query(del(translation.name).where({ '`textId`': id }).toString());

    response = {
      body: JSON.stringify({ data: true }),
      headers,
      statusCode: 204,
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
