const newId = require('../newId');
const cacheKey = require('./cacheKey');

describe('cacheKey.js', () => {
  describe('#cacheKey', () => {
    it('정상적인 파라미터를 받았을 때', () => {
      const id = newId();

      expect(cacheKey(id, {})).toBe(id);
      expect(cacheKey(id, { b: 0.8, c: true })).toBe(`b=0.8,c=true/${id}`);
      expect(cacheKey(id, { invalid: 'params', c: true })).toBe(`c=true/${id}`);
    });
  });
});
