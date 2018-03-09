import _ from 'lodash';
import { select, insert } from 'sql-bricks';
import put from './put';
import parse from './lib/parse';
import getConnection from './lib/getConnection';

const randomString = (length = 5) => {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  _.forEach(_.range(length), () => {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  });

  return text;
};

describe('put.js', () => {
  let conn;
  let origin;

  beforeEach(async () => {
    conn = await getConnection();
    const { insertId } = await conn.query(insert('style', { component: 'anonymous' }).toString());
    const raw = await conn.query(select().from('style').where({ id: insertId }).toString());
    origin = parse(raw[0]);
  });

  afterEach(async () => {
    await conn.query('TRUNCATE style');
    conn.end();
  });

  it('모든 필드의 수정을 요청했을 때', async () => {
    const expectedBody = randomString(100);
    const expectedActive = true;
    const expectedComponent = randomString(50);

    const body = JSON.stringify({
      body: expectedBody,
      active: expectedActive,
      component: expectedComponent,
    });

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveProperty('id', origin.id);
      expect(data).toHaveProperty('body', expectedBody);
      expect(data).toHaveProperty('active', expectedActive);
      expect(data).toHaveProperty('component', expectedComponent);
    };

    return put({ pathParameters: { id: origin.id }, body }, null, callback);
  });

  it('일부 필드의 수정만 요청했을 때', async () => {
    const expectedBody = randomString(100);

    const body = JSON.stringify({
      body: expectedBody,
    });

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveProperty('id', origin.id);
      expect(data).toHaveProperty('body', expectedBody);
      expect(data).toHaveProperty('active', false);
      expect(data).toHaveProperty('component', 'anonymous');
    };

    return put({ pathParameters: { id: origin.id }, body }, null, callback);
  });

  it('빈 본문으로 요청했을 때', () => {
    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveProperty('id', origin.id);
      expect(data).toHaveProperty('body', null);
      expect(data).toHaveProperty('active', false);
      expect(data).toHaveProperty('component', 'anonymous');
      expect(data).toHaveProperty('createdAt');
      expect(data).toHaveProperty('updatedAt');
    };

    return put({ pathParameters: { id: origin.id }, body: null }, null, callback);
  });

  it('존재하지 않는 필드가 포함되어 있을 때', () => {
    const body = JSON.stringify({
      nonexistentField: 'nonexistentField',
    });

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveProperty('id', origin.id);
      expect(data).toHaveProperty('body', null);
      expect(data).toHaveProperty('active', false);
      expect(data).toHaveProperty('component', 'anonymous');
      expect(data).toHaveProperty('createdAt');
      expect(data).toHaveProperty('updatedAt');
    };

    return put({ pathParameters: { id: origin.id }, body }, null, callback);
  });
});
