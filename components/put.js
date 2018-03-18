import _ from 'lodash';
import { select, update } from 'sql-bricks';
import style from './lib/table';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const { id } = e.pathParameters;
  const { name, columns } = style;
  const omitted = _.keys(_.omit(columns, ['id', 'createdAt', 'updatedAt']));
  const picked = _.pick(JSON.parse(e.body), omitted);

  if (picked.key) {
    picked[columns.key] = picked.key;
    delete picked.key;
  }

  const sql = update(name, parse(picked)).where({ id });
  const conn = await getConnection();

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    if (!_.isEmpty(picked)) {
      await conn.query(sql.toString());
    }

    const data = await conn.query(select().from(name).where({ id }).toString());
    const parsed = parse(data[0], true);

    response = {
      body: JSON.stringify({ data: parsed }),
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
