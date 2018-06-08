const _ = require('lodash');
const sharp = require('sharp');
const AWS = require('aws-sdk');
const { select } = require('sql-bricks');
const table = require('./lib/table');
const abort = require('./lib/abort');
const parse = require('./lib/parse');
const parseError = require('./lib/parse/error');
const parseCacheKey = require('./lib/parse/cacheKey');
const parseQueryParam = require('./lib/parse/queryParam');
const { getConnection, getRedis } = require('./lib/getConnection');

AWS.config.update({
  accessKeyId: 'AKIAIN3HLHS26Z4CLVUA',
  secretAccessKey: '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',
});
AWS.config.setPromisesDependency(Promise);

exports.handler = async (e, context, callback) => {
  const s3 = new AWS.S3();
  const conn = await getConnection();
  const redis = getRedis();
  const { id } = _.get(e, 'pathParameters') || {};
  const { name, columns } = table;
  const queryParams = _.get(e, 'queryStringParameters');
  const { b, c, h, q, w } = parseQueryParam(queryParams); // eslint-disable-line max-len, object-curly-newline
  const cacheKey = parseCacheKey(id, queryParams);

  if (cacheKey === id) {
    conn.end();
    redis.client.end(true);

    callback(null, {
      headers: { Location: `https://static.wslo.co/files/${id}` },
      statusCode: 301,
    });

    return;
  }

  let cacheValue = await redis.get(cacheKey);

  if (cacheValue) {
    conn.end();
    redis.client.end(true);

    callback(null, {
      headers: { Location: cacheValue },
      statusCode: 301,
    });

    return;
  }

  let response;

  try {
    const sql = select().from(name).where(columns.id, id);
    const data = _.first(await conn.query(sql.toString()));
    const parsed = await parse(data, true);

    if (_.isNil(data)) {
      throw abort(404, 'not found');
    }

    if (!_.startsWith(parsed.type, 'image/')) {
      throw abort(500, 'not image');
    }

    const origin = await s3.getObject({
      Bucket: 'static.wslo.co',
      Key: `files/${parsed.id}`,
    }).promise();

    let target = sharp(origin.Body);

    // quality
    if (q) {
      target = target.jpeg({ quality: _.toNumber(q) * 100 });
    } else {
      target = target.jpeg();
    }

    // resize
    if (w || h) {
      const width = _.toNumber(w) || undefined;
      const height = _.toNumber(h) || undefined;

      target = target.resize(width, height);
    }

    // crop
    if (_.toLower(c) !== 'true') {
      target = target.max();
    }

    // blur
    if (b) {
      target = target.blur(_.toNumber(b) * 1000);
    }

    await s3.putObject({
      Bucket: 'static.wslo.co',
      Key: `files-cache/${cacheKey}`,
      Body: await target.toBuffer(),
      ACL: 'public-read',
      ContentType: parsed.type,
      ContentDisposition: `attachment; filename="${parsed.name}"`,
    }).promise();

    cacheValue = `https://static.wslo.co/files-cache/${cacheKey}`;
    await redis.set(cacheKey, cacheValue);

    response = {
      headers: { Location: cacheValue },
      statusCode: 301,
    };
  } catch (error) {
    response = {
      body: JSON.stringify({ error: parseError(error) }),
      headers: { 'Access-Control-Allow-Origin': '*' },
      statusCode: error.statusCode || 400,
    };
  } finally {
    conn.end();
    redis.client.end(true);
  }

  callback(null, response);
};
