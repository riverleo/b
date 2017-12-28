// 참고
// https://devstarsj.github.io/2017/04/08/AWS-Lambda-BinaryResponse/

const AWS = require('aws-sdk');
const sharp = require('sharp');

const s3 = new AWS.S3({
  accessKeyId: process.env.ACCESS_KEY_ID,
  secretAccessKey: process.env.SECRET_ACCESS_KEY,
  region: 'ap-northeast-2',
});

const toResponse = (bytes, data) => ({
  statusCode: 200,
  headers: {
    'etag': data.ETag,
    'content-type': data.ContentType,
    'cache-control': 'max-age=2628000',
    'last-modified': data.LastModified,
    'content-length': data.ContentLength,
  },
  body: bytes.toString("base64"),
  isBase64Encoded: true,
});

const getByKey = (e, context, callback) => {
  const { key } = e.pathParameters || {};
  const { s, aspectRatio } = e.queryStringParameters || {};
  const originKey = `origin/${key}`;
  const isAspectRatio = aspectRatio === '1' || aspectRatio === 'true';
  const transformKey = `${s}${isAspectRatio ? '_aspectRatio' : ''}/${key}`;

  let width;
  let height;
  let isOrigin = true;

  if (typeof(s) === 'string') {
    const matched = s.match(/^([0-9]+)?x([0-9]+)?$/);

    if (matched) {
      width = parseInt(matched[1], 10) || undefined;
      height = parseInt(matched[2], 10) || undefined;

      if (width || height) {
        isOrigin = false;
      }
    }
  }

  const params = {
    Bucket: 'static.scdc.co',
    Key: isOrigin ? originKey : transformKey,
  };

  s3.getObject(params, (err, data) => {
    if (isOrigin && err) {
      callback(null, err);
      return;
    }

    if (data) {
      callback(null, toResponse(data.Body, data));
      return;
    }

    s3.getObject({
      Bucket: 'static.scdc.co',
      Key: originKey,
    }, (err, data) => {
      let s = sharp(data.Body).resize(width, height)

      if (isAspectRatio) {
        s = s.max();
      }

      s.toBuffer()
        .then((resized) => s3.putObject({
          ACL: 'public-read',
          Key: transformKey,
          Body: resized,
          ContentType: data.ContentType,
          Bucket: 'static.scdc.co',
        }, () => callback(null, toResponse(resized, data))))
        .catch(err => callback(null, err));
    });
  });
}

module.exports = getByKey;
