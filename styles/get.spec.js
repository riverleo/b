import _ from 'lodash';
import { insert } from 'sql-bricks';
import get from './get';
import getConnection from './lib/getConnection';

describe('get.js', () => {
  let conn;

  beforeEach(async () => {
    conn = await getConnection();
    await conn.query('TRUNCATE style');
  });

  afterEach(async () => {
    await conn.query('TRUNCATE style');
    conn.end();
  });

  it('전체 스타일시트들을 불러올 때', async () => {
    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp2' }).toString());
    await conn.query(insert('style', { component: 'comp3' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
    };

    return get({}, null, callback);
  });

  it('특정 컴포넌트의 스타일시트들만 불러올 때', async () => {
    const expectedComponent = 'expectedComponent';

    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(1);
      expect(data[0]).toHaveProperty('component', expectedComponent);
    };

    return get({ queryStringParameters: { component: expectedComponent } }, null, callback);
  });
});
