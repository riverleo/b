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

    const textTable = table.text.name;
    const translationTable = table.translation.name;
    const {
      id: idColumn,
      key: keyColumn,
      createdAt: createdAtColumn,
    } = table.text.columns;
    const {
      body: bodyColumn,
      lcid: lcidColumn,
      textId: textIdColumn,
    } = table.translation.columns;

    const textParams = { [keyColumn]: picked.key };
    let text = _.first(await conn.query(select().from(textTable).where(textParams).toString()));

    if (_.isNil(text)) {
      const { insertId: textId } = await conn.query(insert(textTable, textParams).toString());
      text = _.first(await conn.query(select().from(textTable).where({ id: textId }).toString()));
    }

    const translationParams = { [lcidColumn]: picked.lcid, [textIdColumn]: text.id };
    const translationSelectSQL = select().from(translationTable).where(translationParams);
    const translation = _.first(await conn.query(translationSelectSQL.toString()));

    if (_.isNil(translation)) {
      await conn.query(insert(
        translationTable,
        _.assign({}, translationParams, { [bodyColumn]: picked.body }),
      ).toString());
    } else {
      await conn.query(update(
        translationTable,
        _.assign({}, translationParams, { [bodyColumn]: picked.body }),
      ).toString());
    }

    const data = await conn.query(select().from(textTable)
      .join(translationTable, { [textIdColumn]: idColumn })
      .where({ [textIdColumn]: text.id })
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
