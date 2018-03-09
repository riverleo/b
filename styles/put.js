import _ from 'lodash';
import { select, update } from 'sql-bricks';
import { TABLE, COLUMNS } from './lib/constants';
import parse, { parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const { id } = e.pathParameters;
  const { COMPONENT, BODY, ACTIVE } = COLUMNS;
  const picked = _.pick(JSON.parse(e.body), [COMPONENT, BODY, ACTIVE]);
  const sql = update(TABLE, parse(picked)).where({ id });
  const conn = await getConnection();

  let response;

  try {
    if (!_.isEmpty(picked)) {
      await conn.query(sql.toString());
    }

    const data = await conn.query(select().from(TABLE).where({ id }).toString());

    response = {
      statusCode: 200,
      body: JSON.stringify({ data: parse(data[0], true) }),
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
