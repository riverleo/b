import _ from 'lodash';
import { select, insert } from 'sql-bricks';
import component from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const { name, columns } = component;
  const omitted = _.keys(_.omit(columns, ['id', 'createdAt', 'updatedAt']));
  const picked = _.pick(JSON.parse(e.body), omitted);
  const conn = await getConnection();

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  if (picked.key) {
    picked[columns.key] = picked.key;
    delete picked.key;
  }

  try {
    const { insertId } = await conn.query(insert(name, parse(picked, true)).toString());
    const data = await conn.query(select().from(name).where({ id: insertId }).toString());

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
