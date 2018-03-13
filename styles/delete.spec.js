import { select, insert } from 'sql-bricks';
import del from './delete';
import parse from './lib/parse';
import getConnection from './lib/getConnection';

describe('delete.js', () => {
  let conn;
  let origin;

  beforeEach(async () => {
    conn = await getConnection();
    await conn.query('TRUNCATE style');
    const { insertId } = await conn.query(insert('style', { component: 'anonymous' }).toString());
    const raw = await conn.query(select().from('style').where({ id: insertId }).toString());
    origin = parse(raw[0]);
  });

  afterEach(async () => {
    await conn.query('TRUNCATE style');
    conn.end();
  });

  it('데이터를 삭제를 요청할 때', async () => {
    let finded = await conn.query(select().from('style').where({ id: origin.id }).toString());

    expect(finded).toHaveLength(1);

    const callback = async (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toBe(true);

      finded = await conn.query(select().from('style').where({ id: origin.id }).toString());
      expect(finded).toHaveLength(0);
    };

    return del({ pathParameters: { id: origin.id } }, null, callback);
  });

  it('존재하지 않는 데이터의 삭제를 요청할 때', () => {
    const callback = async (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toBe(true);
    };

    return del({ pathParameters: { id: 77777 } }, null, callback);
  });
});
