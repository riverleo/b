'use strict';

const getByKey = require('./methods/getByKey');

exports.handle = (event, context, callback) => {
  getByKey(event, context, callback);
};
