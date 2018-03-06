import _ from 'lodash';
import mysql from 'promise-mysql';
import { select } from 'sql-bricks';
import db from './db.json';

export default async (e, context, callback) => {
  let data = [];
  const conn = await mysql.createConnection(db[process.env.NODE_ENV || 'prod']);

  try {
    const params = _.get(e, 'queryStringParameters') || {};
    let query = select().from('style').orderBy('createdAt DESC');

    if (!_.isNil(params.active)) {
      query = query.where('active', _.toLower(params.active) === 'true' ? true : false);
    }

    if (!_.isNil(params.component)) {
      query = query.where('component', params.component);
    }

    data = await conn.query(query.toString());

    _.forEach(data, (style) => { style.active = !!style.active; });
  }
  catch (e) {
    throw e;
  }
  finally {
    conn.end();
  }

  callback(null, {
    statusCode: 200,
    body: JSON.stringify({ data }),
  });
};
