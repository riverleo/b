import mysql from 'promise-mysql';
import db from '../db.json';

export default () => mysql.createConnection(db[process.env.NODE_ENV || 'prod']);
