import { insert } from 'sql-bricks';
import table from './lib/table';
import get from './get';
import getConnection from './lib/getConnection';

describe('get.js', () => {
  let conn;

  beforeEach(async () => {
    conn = await getConnection();
    await conn.query('TRUNCATE component');
  });

  afterEach(async () => {
    await conn.query('TRUNCATE component');
    conn.end();
  });

  it('전체 스타일시트들을 불러올 때', async () => {
    await conn.query(insert(table.name, { '`key`': 'comp1' }).toString());
    await conn.query(insert(table.name, { '`key`': 'comp2' }).toString());
    await conn.query(insert(table.name, { '`key`': 'comp3' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
    };

    return get({}, null, callback);
  });

  it('특정 컴포넌트의 스타일시트들만 불러올 때', async () => {
    const expectedKey = 'expectedKey';

    await conn.query(insert(table.name, { '`key`': 'comp1' }).toString());
    await conn.query(insert(table.name, { '`key`': expectedKey }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(1);
      expect(data[0]).toHaveProperty('key', expectedKey);
    };

    return get({ queryStringParameters: { key: expectedKey } }, null, callback);
  });
});
