import _ from 'lodash';
import { insert } from 'sql-bricks';
import get from './get';
import getConnection from './lib/getConnection';

describe('get.js', () => {
  let conn;

  beforeEach(async () => {
    conn = await getConnection();
    await conn.query('TRUNCATE locale');
  });

  afterEach(async () => {
    await conn.query('TRUNCATE locale');
    conn.end();
  });

  it('전체 지역정보를 불러올 때', async () => {
    await conn.query(insert('locale', { language: 'ko', country: 'KR' }).toString());
    await conn.query(insert('locale', { language: 'en', country: 'US' }).toString());
    await conn.query(insert('locale', { language: 'ja', country: 'JP' }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
    };

    return get({}, null, callback);
  });

  it('활성화된 지역정보만 불러올 때', async () => {
    await conn.query(insert('locale', { language: 'ko', country: 'KR' }).toString());
    await conn.query(insert('locale', { language: 'en', country: 'US' }).toString());
    await conn.query(insert('locale', { language: 'ja', country: 'JP' }).toString());
    await conn.query(insert('locale', { language: 'en', country: 'GB', active: true }).toString());
    await conn.query(insert('locale', { language: 'zh', country: 'CN', active: true }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(2);
      _.forEach(data, locale => expect(locale).toHaveProperty('active', true));
    };

    return get({ queryStringParameters: { active: 'true' } }, null, callback);
  });

  it('비활성화된 지역정보만 불러올 때', async () => {
    await conn.query(insert('locale', { language: 'ko', country: 'KR' }).toString());
    await conn.query(insert('locale', { language: 'en', country: 'US' }).toString());
    await conn.query(insert('locale', { language: 'ja', country: 'JP' }).toString());
    await conn.query(insert('locale', { language: 'en', country: 'GB', active: true }).toString());
    await conn.query(insert('locale', { language: 'zh', country: 'CN', active: true }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(3);
      _.forEach(data, locale => expect(locale).toHaveProperty('active', false));
    };

    return get({ queryStringParameters: { active: 'false' } }, null, callback);
  });

  it('특정 국가의 지역정보만 불러올 때', async () => {
    const expectedCountry = 'CN';

    await conn.query(insert('locale', { language: 'ko', country: 'KR' }).toString());
    await conn.query(insert('locale', { language: 'en', country: 'US' }).toString());
    await conn.query(insert('locale', { language: 'ja', country: 'JP' }).toString());
    await conn.query(insert('locale', { language: 'zh', country: expectedCountry }).toString());
    await conn.query(insert('locale', { language: 'nl', country: expectedCountry }).toString());
    await conn.query(insert('locale', { language: 'af', country: expectedCountry }).toString());
    await conn.query(insert('locale', { language: 'sk', country: expectedCountry }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(4);
      _.forEach(data, locale => expect(locale).toHaveProperty('country', expectedCountry));
    };

    return get({ queryStringParameters: { country: expectedCountry } }, null, callback);
  });

  it('특정 언어의 지역정보만 불러올 때', async () => {
    const expectedLanguage = 'zh';

    await conn.query(insert('locale', { language: 'ko', country: 'KR' }).toString());
    await conn.query(insert('locale', { language: 'en', country: 'US' }).toString());
    await conn.query(insert('locale', { language: 'ja', country: 'JP' }).toString());
    await conn.query(insert('locale', { language: expectedLanguage, country: 'GB' }).toString());
    await conn.query(insert('locale', { language: expectedLanguage, country: 'CN' }).toString());
    await conn.query(insert('locale', { language: expectedLanguage, country: 'PR' }).toString());
    await conn.query(insert('locale', { language: expectedLanguage, country: 'SK' }).toString());
    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(4);
      _.forEach(data, locale => expect(locale).toHaveProperty('language', expectedLanguage));
    };

    return get({ queryStringParameters: { language: expectedLanguage } }, null, callback);
  });

  it('특정 국가와 언어의 지역정보만 불러올 때', async () => {
    const expectedCountry = 'es';
    const expectedLanguage = 'PR';

    await conn.query(insert('locale', { language: 'ko', country: 'KR' }).toString());
    await conn.query(insert('locale', { language: expectedLanguage, country: 'US' }).toString());
    await conn.query(insert('locale', { language: expectedLanguage, country: 'JP' }).toString());
    await conn.query(insert('locale', { language: expectedLanguage, country: expectedCountry }).toString());
    await conn.query(insert('locale', { language: 'zh', country: expectedCountry }).toString());
    await conn.query(insert('locale', { language: 'nl', country: expectedCountry }).toString());
    await conn.query(insert('locale', { language: 'af', country: expectedCountry }).toString());

    const callback = (err, result) => {
      const { data } = JSON.parse(result.body);

      expect(data).toHaveLength(1);
      expect(data[0]).toHaveProperty('country', expectedCountry);
      expect(data[0]).toHaveProperty('language', expectedLanguage);
    };

    return get({
      queryStringParameters: {
        country: expectedCountry,
        language: expectedLanguage,
      },
    }, null, callback);
  });
});
