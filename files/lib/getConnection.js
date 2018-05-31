/* global process */

const redis = require('redis');
const mysql = require('promise-mysql');
const { promisify } = require('util');
const db = require('../db.json');

exports.getRedis = () => {
  const client = redis.createClient(db[process.env.NODE_ENV].redis);
  const getAsync = promisify(client.get).bind(client);
  const setAsync = promisify(client.set).bind(client);

  return {
    client,
    get: getAsync,
    set: setAsync,
  };
};

exports.getConnection = () => mysql.createConnection(db[process.env.NODE_ENV].mysql);
