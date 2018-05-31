const _ = require('lodash');
const parseQueryParam = require('./queryParam');

module.exports = (id, rawQueryParams) => {
  const queryParams = parseQueryParam(rawQueryParams);

  let prefix;

  if (!_.isEmpty(queryParams)) {
    prefix = _.map(queryParams, (v, k) => (_.isNil(v) ? '' : `${k}=${v}`));
    prefix = `${_.join(_.compact(prefix), ',')}`;
  }

  return prefix ? `${prefix}/${id}` : id;
};
