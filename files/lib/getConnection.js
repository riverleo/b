import redis from 'redis';
import mysql from 'promise-mysql';
import { promisify } from 'util';
import db from '../db.json';

export const getRedis = () => {
  const client = redis.createClient(db[process.env.NODE_ENV].redis);
  const getAsync = promisify(client.get).bind(client);
  const setAsync = promisify(client.set).bind(client);

  return {
    get: getAsync,
    set: setAsync,
  };
};

export default () => mysql.createConnection(db[process.env.NODE_ENV].mysql);
