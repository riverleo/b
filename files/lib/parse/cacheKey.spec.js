import newId from '../newId';
import cacheKey from './cacheKey';

describe('cacheKey.js', () => {
  describe('#cacheKey', () => {
    it('정상적인 파라미터를 받았을 때', () => {
      expect(cacheKey(newId(), { b: 0.8, c: true })).toBe('"b=0.8,c=true/eM0bXZOtZED"');
      expect(cacheKey(newId(), { invalid: 'params', c: true })).toBe('"c=true/eM0bXZOtZED"');
    });
  });
});
