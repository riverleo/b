const _ = require('lodash');
const AWS = require('aws-sdk');
const Promise = require('bluebird');
const { select, insert, in: $in } = require('sql-bricks');
const newId = require('./lib/newId');
const table = require('./lib/table');
const parse = require('./lib/parse');
const parseError = require('./lib/parse/error');
const { getConnection } = require('./lib/getConnection');
const parseFormData = require('./lib/parse/formData');

AWS.config.update({
  accessKeyId: 'AKIAIN3HLHS26Z4CLVUA',
  secretAccessKey: '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',
});
AWS.config.setPromisesDependency(Promise);

exports.handler = async (e, context, callback) => {
  const s3 = new AWS.S3();
  const conn = await getConnection();
  const files = _.values(parseFormData(e, true));
  const { name, columns } = table;

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    const ids = await Promise.map(files, async (file) => {
      const id = newId(64);
      const parsed = parse({ id, ..._.omit(file, ['type']) });

      await s3.putObject({
        Bucket: 'static.wslo.co',
        Key: `files/${id}`,
        Body: file.content,
        ACL: 'public-read',
        ContentType: parsed.type,
        ContentDisposition: `attachment; filename="${parsed.name}"`,
      }).promise();

      await conn.query(insert(name, parsed).toString());

      return id;
    });

    const sql = select().from(name).where($in(columns.id, ids));
    const data = await conn.query(sql.toString());

    response = {
      body: JSON.stringify({ data }),
      headers,
      statusCode: 200,
    };
  } catch (error) {
    response = {
      body: JSON.stringify({ error: parseError(error) }),
      headers,
      statusCode: error.statusCode || 400,
    };
  } finally {
    conn.end();
  }

  callback(null, response);
};
