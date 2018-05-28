import _ from 'lodash';
import AWS from 'aws-sdk';
import Promise from 'bluebird';
import { select, insert, in as $in } from 'sql-bricks';
import newId from './lib/newId';
import table from './lib/table';
import parse from './lib/parse';
import getConnection from './lib/getConnection';
import parseFormData from './lib/parse/formData';
import parseSQLError from './lib/parse/sqlError';

AWS.config.update({
  accessKeyId: 'AKIAIN3HLHS26Z4CLVUA',
  secretAccessKey: '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',
});
AWS.config.setPromisesDependency(Promise);

export default async (e, context, callback) => {
  const s3 = new AWS.S3();
  const conn = await getConnection();
  const files = _.values(parseFormData(e, true));
  const { name, columns } = table;

  let response;
  const headers = { 'Access-Control-Allow-Origin': '*' };

  try {
    const ids = await Promise.map(files, async (file) => {
      const id = newId(64);

      await s3.putObject({
        Bucket: 'static.wslo.co',
        Key: `files/${id}`,
        Body: file.content,
        ACL: 'public-read',
        ContentType: file.contentType,
        ContentDisposition: `attachment; filename="${file.filename}"`,
      }).promise();

      await conn.query(insert(name, parse({ id, ...file })).toString());

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
      body: JSON.stringify({ error: parseSQLError(error) }),
      headers,
      statusCode: error.statusCode || 400,
    };
  } finally {
    conn.end();
  }

  callback(null, response);
};
