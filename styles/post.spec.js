import post from './post';
import getConnection from './lib/getConnection';

describe('post.js', () => {
  let conn;

  beforeEach(async () => {
    conn = await getConnection();
  });

  afterEach(async () => {
    await conn.query('TRUNCATE style');
    conn.end();
  });

  it('정상적인 본문으로 요청했을 때', () => {
    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveProperty('id');
      expect(data).toHaveProperty('body');
      expect(data).toHaveProperty('active');
      expect(data).toHaveProperty('component');
      expect(data).toHaveProperty('createdAt');
      expect(data).toHaveProperty('updatedAt');
    };

    return post({ body: JSON.stringify({ component: 'comp' }) }, null, callback);
  });

  it('빈 본문으로 요청했을 때', () => {
    const callback = (err, result) => {
      const { error } = JSON.parse(result.body);

      expect(error.code).toBeDefined();
      expect(error.message).toBeDefined();
    };

    return post({ body: null }, null, callback);
  });
});
