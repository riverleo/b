import _ from 'lodash';
import { select, update, and, notEq } from 'sql-bricks';
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
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    if (!_.isEmpty(picked)) {
      await conn.query(sql.toString());
    }

    const data = await conn.query(select().from(TABLE).where({ id }).toString());
    const style = parse(data[0], true);

    if (picked.active) {
      const sql = update(TABLE, { active: false }).where(and({ component: style.component }, notEq('id', id)));
      await conn.query(sql.toString());
    }

    response = {
      body: JSON.stringify({ data: style }),
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
