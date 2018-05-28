import _ from 'lodash';
import parseQueryParam from './queryParam';

export default (id, rawQueryParams) => {
  const queryParams = parseQueryParam(rawQueryParams);

  let prefix = 'origin';

  if (!_.isEmpty(queryParams)) {
    prefix = _.join(_.map(queryParams, (v, k) => `${k}=${v}`), ',');
  }

  return `${prefix}/${id}`;
};
