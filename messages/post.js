import _ from 'lodash';
import { select, insert, update } from 'sql-bricks';
import table from './lib/table';
import parse, { newError, parseSQLError } from './lib/parse';
import getConnection from './lib/getConnection';

export default async (e, context, callback) => {
  const conn = await getConnection();
  const picked = _.pick(JSON.parse(e.body), ['key', 'body', 'lcid']);

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    if (_.isNil(picked.key)) {
      throw newError('`key` parameter is required');
    }

    if (_.isNil(picked.lcid)) {
      throw newError('`lcid` parameter is required');
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
        _.assign({}, tslParams, { [bodyColumn]: picked.body }),
      ).toString());
    }

    const data = await conn.query(select().from(msgTable)
      .join(tslTable, { [msgIdColumn]: idColumn })
      .where({ [msgIdColumn]: message.id })
      .orderBy(`${createdAtColumn} DESC`)
      .toString());

    response = {
      body: JSON.stringify({ data: parse(data, true) }),
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
