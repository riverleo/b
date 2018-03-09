import { delete as del } from 'sql-bricks';
import { TABLE } from './lib/constants';
import { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const { id } = e.pathParameters;
  const sql = del(TABLE).where({ id });
  const conn = await getConnection();

  let response;

  try {
    await conn.query(sql.toString());

    response = {
      statusCode: 204,
      body: JSON.stringify({ data: true }),
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
