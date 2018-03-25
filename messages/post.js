import _ from 'lodash';
import Promise from 'bluebird';
import { select, insert, update } from 'sql-bricks';
import table from './lib/table';
import parse, { newError, parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

const upsert = async (conn, body) => {
  const picked = _.pick(body, ['key', 'body', 'lcid']);

  if (_.isNil(picked.key)) {
    throw newError('`key` parameter is required');
  }

  const msgTable = table.message.name;
  const tslTable = table.translation.name;
  const {
    id: idColumn,
    key: keyColumn,
    createdAt: createdAtColumn,
  } = table.message.columns;
  const {
    body: bodyColumn,
    lcid: lcidColumn,
    messageId: msgIdColumn,
  } = table.translation.columns;

  const msgParams = { [keyColumn]: picked.key };
  let message = _.first(await conn.query(select().from(msgTable).where(msgParams).toString()));

  if (_.isNil(message)) {
    const { insertId: msgId } = await conn.query(insert(msgTable, msgParams).toString());
    message = _.first(await conn.query(select().from(msgTable).where({ id: msgId }).toString()));
  }

  if (!_.isNil(picked.lcid)) {
    const tslParams = { [lcidColumn]: picked.lcid, [msgIdColumn]: message.id };
    const tslSelectSQL = select().from(tslTable).where(tslParams);
    const translation = _.first(await conn.query(tslSelectSQL.toString()));

    if (_.isNil(translation)) {
      await conn.query(insert(
        tslTable,
        _.assign({}, tslParams, { [bodyColumn]: picked.body }),
      ).toString());
    } else {
      await conn.query(update(
        tslTable,
        { [bodyColumn]: picked.body },
      ).where({
        [lcidColumn]: picked.lcid,
        [msgIdColumn]: message.id,
      }).toString());
    }
  }

  const data = await conn.query(select([
    table.message.columns.id,
    table.message.columns.key,
    table.translation.columns.body,
    table.translation.columns.lcid,
  ]).from(msgTable)
    .leftJoin(tslTable, { [msgIdColumn]: idColumn })
    .where({ [idColumn]: message.id })
    .orderBy(`${createdAtColumn} DESC`)
    .toString());

  return parse(data, true);
};

export default async (e, context, callback) => {
  const conn = await getConnection();
  const body = JSON.parse(e.body);

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    let data;

    if (_.isArray(body)) {
      data = await Promise.map(body, p => upsert(conn, p));
    } else {
      data = await upsert(conn, body);
    }

    response = {
      body: JSON.stringify({ data }),
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
