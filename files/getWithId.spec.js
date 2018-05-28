import getWithId from './getWithId';
import getConnection from './lib/getConnection';

describe('get.js', () => {
  let conn;

  beforeEach(async () => {
    conn = await getConnection();
    await conn.query('TRUNCATE file');
  });

  afterEach(async () => {
    await conn.query('TRUNCATE file');
    conn.end();
  });

  it('test', () => {
    getWithId();
  });
});
