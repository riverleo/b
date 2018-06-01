const _ = require('lodash');
const abort = require('../abort');
const newId = require('../newId');

const getValueIgnoreCase = (obj, lookedKey) => {
  const key = _.find(_.keys(obj), k => _.toLower(k) === _.toLower(lookedKey));

  return obj[key];
};

module.exports = (e) => {
  const boundary = _.split(getValueIgnoreCase(e.headers, 'Content-Type'), 'boundary=')[1];
  const body = (e.isBase64Encoded ? Buffer.from(e.body, 'base64').toString('binary') : e.body);

  if (_.isNil(boundary)) {
    throw abort(500, 'invalid form');
  }

  const rawFormData = _.filter(_.split(body, boundary), r => _.includes(r, 'Content-Disposition: form-data'));

  const result = {};

  _.forEach(rawFormData, (raw) => {
    let name, type, filename, contentType;

    const nameExecuted = /name=\"([^\"]*)\"/.exec(raw);
    const filenameExecuted = /filename=\"([^\"]*)\"/.exec(raw);
    const contentTypeExecuted = /Content-Type: ([a-zA-Z0-9\/]*)/.exec(raw);
    let content = _.split(_.split(raw, /\r\n\r\n/)[1], /\r\n--/)[0];

    if (!_.isNil(nameExecuted) && !_.isEmpty(nameExecuted[1])) {
      name = nameExecuted[1];
    } else {
      name = newId();
    }

    if (!_.isNil(filenameExecuted)) {
      filename = filenameExecuted[1];
    }

    if (!_.isNil(contentTypeExecuted)) {
      type = 'file';
      content = Buffer.from(content, 'binary');
    } else {
      type = 'text';
    }

    if (!_.isNil(contentTypeExecuted)) {
      contentType = contentTypeExecuted[1];
    }

    result[name] = {
      type,
      filename,
      contentType,
      content,
    };
  });

  return result;
};
