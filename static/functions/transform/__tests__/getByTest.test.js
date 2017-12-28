const getByKey = require('../methods/getByKey');

describe('getByKey', () => {
  it('should get s3 object', () => {
    const e = {
      pathParameters: {
        key: 'test.jpg',
      },
    };

    const callback = (__, { headers, body, statusCode }) => {
      expect(statusCode).toBe(200);
      expect(body).toBeDefined();
      expect(headers['etag']).toBeDefined();
      expect(headers['content-type']).toBe('image/jpeg');
      expect(headers['last-modified']).toBeDefined();
    };

    getByKey(e, null, callback);
  });
});
