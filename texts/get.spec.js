import _ from 'lodash';
import { insert } from 'sql-bricks';
import get from './get';
import getConnection from './lib/getConnection';

describe('get.js', () => {
  let conn;

  beforeEach(async () => {
    conn = await getConnection();
    await conn.query('TRUNCATE text');
    await conn.query('TRUNCATE translation');
  });

  afterEach(async () => {
    await conn.query('TRUNCATE text');
    await conn.query('TRUNCATE translation');
    conn.end();
  });

  it('전체 텍스트들을 불러올 때', async () => {
    const t1 = await conn.query(insert('text', { '`key`': 't1' }).toString());
    await conn.query(insert('translation', { '`textId`': t1.insertId, body: 'body', lcid: 'ko_KR' }).toString());
    const t2 = await conn.query(insert('text', { '`key`': 't2' }).toString());
    await conn.query(insert('translation', { '`textId`': t2.insertId, body: 'body', lcid: 'ko_KR' }).toString());
    const t3 = await conn.query(insert('text', { '`key`': 't3' }).toString());
    await conn.query(insert('translation', { '`textId`': t3.insertId, body: 'body', lcid: 'ko_KR' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
    };

    return get({}, null, callback);
  });

  it('`lcid` 파라미터로 텍스트들을 불러올 때', async () => {
    const t1 = await conn.query(insert('text', { '`key`': 't1' }).toString());
    await conn.query(insert('translation', { '`textId`': t1.insertId, body: 'body', lcid: 'ko_KR' }).toString());
    await conn.query(insert('translation', { '`textId`': t1.insertId, body: 'body', lcid: 'en_US' }).toString());
    const t2 = await conn.query(insert('text', { '`key`': 't2' }).toString());
    await conn.query(insert('translation', { '`textId`': t2.insertId, body: 'body', lcid: 'en_US' }).toString());
    const t3 = await conn.query(insert('text', { '`key`': 't3' }).toString());
    await conn.query(insert('translation', { '`textId`': t3.insertId, body: 'body', lcid: 'ko_KR' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(2);
      expect(_.find(data, t => t.key === 't1').translations).toHaveLength(1);
      expect(_.find(data, t => t.key === 't1').translations[0]).toHaveProperty('lcid', 'ko_KR');
      expect(_.find(data, t => t.key === 't3').translations).toHaveLength(1);
      expect(_.find(data, t => t.key === 't3').translations[0]).toHaveProperty('lcid', 'ko_KR');
    };

    return get({ queryStringParameters: { lcid: 'ko_KR' } }, null, callback);
  });

  it('`q` 파라미터로 텍스트들을 불러올 때', async () => {
    const t1 = await conn.query(insert('text', { '`key`': 't1' }).toString());
    await conn.query(insert('translation', { '`textId`': t1.insertId, body: '`le`o', lcid: 'ko' }).toString());
    const t2 = await conn.query(insert('text', { '`key`': 't2' }).toString());
    await conn.query(insert('translation', { '`textId`': t2.insertId, body: 'body', lcid: 'en' }).toString());
    await conn.query(insert('translation', { '`textId`': t2.insertId, body: 'el`le`', lcid: 'ko' }).toString());
    const t3 = await conn.query(insert('text', { '`key`': 't3' }).toString());
    await conn.query(insert('translation', { '`textId`': t3.insertId, body: 'body', lcid: 'ko' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(2);
      expect(_.find(data, t => t.key === 't1').translations).toHaveLength(1);
      expect(_.find(data, t => t.key === 't2').translations).toHaveLength(2);
    };

    return get({ queryStringParameters: { q: 'le' } }, null, callback);
  });
});
