import _ from 'lodash';
import { select, insert } from 'sql-bricks';
import post from './post';
import getConnection from './lib/getConnection';

describe('post.js', () => {
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

  it('정상적인 본문으로 요청했을 때', () => {
    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveProperty('id');
      expect(data).toHaveProperty('key');
      expect(data).toHaveProperty('translations');
    };

    return post({ body: JSON.stringify({ key: 'key', body: 'body', lcid: 'ko_KR' }) }, null, callback);
  });

  it('기존 텍스트를 수정할 때', async () => {
    const { insertId } = await conn.query(insert('text', { '`key`': 'key' }).toString());
    const { insertId: id } = await conn.query(insert('translation', { '`textId`': insertId, body: 'body', lcid: 'ko_KR' }).toString());
    let saved = _.first(await conn.query(select().from('translation').where({ id }).toString()));
    expect(saved).toHaveProperty('body', 'body');

    const callback = async (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveProperty('id');
      expect(data).toHaveProperty('key');
      expect(data).toHaveProperty('translations.0.body', 'new body');

      saved = _.first(await conn.query(select().from('translation').where({ id }).toString()));
      expect(saved).toHaveProperty('body', 'new body');
    };

    return post({ body: JSON.stringify({ key: 'key', body: 'new body', lcid: 'ko_KR' }) }, null, callback);
  });

  it('빈 본문으로 요청했을 때', () => {
    const callback = (err, result) => {
      const { error } = JSON.parse(result.body);

      expect(error).toBeDefined();
    };

    return post({ body: null }, null, callback);
  });

  it('`key` 파라미터가 누락되었을 때', () => {
    const callback = (err, result) => {
      const { error } = JSON.parse(result.body);

      expect(error).toBeDefined();
    };

    return post({ body: JSON.stringify({ body: 'body', lcid: 'ko_KR' }) }, null, callback);
  });

  it('`lcid` 파라미터가 누락되었을 때', () => {
    const callback = (err, result) => {
      const { error } = JSON.parse(result.body);

      expect(error).toBeDefined();
    };

    return post({ body: JSON.stringify({ key: 'key', body: 'body' }) }, null, callback);
  });

  it('`body` 파라미터가 누락되었을 때', () => {
    const callback = (err, result) => {
      const { error } = JSON.parse(result.body);

      expect(error).not.toBeDefined();
    };

    return post({ body: JSON.stringify({ key: 'key', lcid: 'ko_KR' }) }, null, callback);
  });
});
