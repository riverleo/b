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

  it.skip('전체 스타일시트들을 불러올 때', async () => {
    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp2' }).toString());
    await conn.query(insert('style', { component: 'comp3' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
    };

    return get({}, null, callback);
  });

  it.skip('활성화된 스타일시트들만 불러올 때', async () => {
    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp2' }).toString());
    await conn.query(insert('style', { component: 'comp3' }).toString());
    await conn.query(insert('style', { component: 'comp4', active: true }).toString());
    await conn.query(insert('style', { component: 'comp5', active: true }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(2);
      _.forEach(data, style => expect(style).toHaveProperty('active', true));
    };

    return get({ queryStringParameters: { active: 'true' } }, null, callback);
  });

  it.skip('비활성화된 스타일시트들만 불러올 때', async () => {
    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp2' }).toString());
    await conn.query(insert('style', { component: 'comp3' }).toString());
    await conn.query(insert('style', { component: 'comp4', active: true }).toString());
    await conn.query(insert('style', { component: 'comp5', active: true }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
      _.forEach(data, style => expect(style).toHaveProperty('active', false));
    };

    return get({ queryStringParameters: { active: 'false' } }, null, callback);
  });

  it.skip('특정 컴포넌트의 스타일시트들만 불러올 때', async () => {
    const expectedComponent = 'expectedComponent';

    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp1', active: true }).toString());
    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: expectedComponent, active: true }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(4);
      _.forEach(data, style => expect(style).toHaveProperty('component', expectedComponent));
    };

    return get({ queryStringParameters: { component: expectedComponent } }, null, callback);
  });

  it.skip('특정 컴포넌트의 활성화된 스타일시트들만 불러올 때', async () => {
    const expectedComponent = 'expectedComponent';

    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp1', active: true }).toString());
    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: expectedComponent, active: true }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(1);
      expect(data[0]).toHaveProperty('component', expectedComponent);
      expect(data[0]).toHaveProperty('active', true);
    };

    return get({ queryStringParameters: { component: expectedComponent, active: 'true' } }, null, callback);
  });

  it.skip('특정 컴포넌트의 비활성화된 스타일시트들만 불러올 때', async () => {
    const expectedComponent = 'expectedComponent';

    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp1', active: true }).toString());
    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: expectedComponent, active: true }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());
    await conn.query(insert('style', { component: expectedComponent }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
      expect(data[0]).toHaveProperty('component', expectedComponent);
      expect(data[0]).toHaveProperty('active', false);
    };

    return get({ queryStringParameters: { component: expectedComponent, active: 'false' } }, null, callback);
  });

  it.skip('컴포넌트의 비활성화된 스타일시트들만 불러올 때', async () => {
    const expectedComponent = 'expectedComponent';

    await conn.query(insert('style', { component: 'comp1' }).toString());
    await conn.query(insert('style', { component: 'comp1', active: true }).toString());
    await conn.query(insert('style', { component: 'comp2', active: true }).toString());
    await conn.query(insert('style', { component: 'comp3' }).toString());
    await conn.query(insert('style', { component: 'comp4' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(4);
    };

    return get({ queryStringParameters: { groupBy: 'component' } }, null, callback);
  });
});
