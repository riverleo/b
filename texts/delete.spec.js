import _ from 'lodash';
import { select, insert } from 'sql-bricks';
import del from './delete';
import getConnection from './lib/getConnection';

describe('delete.js', () => {
  let conn;
  let text;

  beforeEach(async () => {
    conn = await getConnection();
    await conn.query('TRUNCATE text');
    await conn.query('TRUNCATE translation');
    const { insertId } = await conn.query(insert('text', { '`key`': 'key' }).toString());
    await conn.query(insert('translation', { '`textId`': insertId, body: 'body', lcid: 'ko_KR' }).toString());

    text = _.first(await conn.query(select().from('text').where({ id: insertId }).toString()));
    await conn.query(select().from('translation').where({ '`textId`': insertId }).toString());
  });

  afterEach(async () => {
    await conn.query('TRUNCATE text');
    await conn.query('TRUNCATE translation');
    conn.end();
  });

  it('데이터를 삭제를 요청할 때', async () => {
    let foundText = await conn.query(select().from('text').where({ id: text.id }).toString());
    let foundTranslation = await conn.query(select().from('translation').where({ '`textId`': text.id }).toString());

    expect(foundText).toHaveLength(1);
    expect(foundTranslation).toHaveLength(1);

    const callback = async (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toBe(true);

      foundText = await conn.query(select().from('text').where({ id: text.id }).toString());
      foundTranslation = await conn.query(select().from('translation').where({ '`textId`': text.id }).toString());

      expect(foundText).toHaveLength(0);
      expect(foundTranslation).toHaveLength(0);
    };

    return del({ pathParameters: { id: text.id } }, null, callback);
  });

  it('존재하지 않는 데이터의 삭제를 요청할 때', () => {
    const callback = async (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toBe(true);
    };

    return del({ pathParameters: { id: 77777 } }, null, callback);
  });
});
