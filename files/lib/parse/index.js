const _ = require('lodash');

module.exports = ({
  id,
  name: _name,
  type: _type,
  bytes: _bytes,
  content,
  filename,
  contentType,
  attachableId,
  attachableType,
}, isAllowNilValue, nullValue = null) => {
  const name = _name || filename;
  const type = _type || contentType;
  const bytes = _bytes || content.byteLength;

  const parsed = {
    id,
    name: !_.isNil(name) ? name : nullValue,
    type: !_.isNil(type) ? type : nullValue,
    bytes: !_.isNil(bytes) ? bytes : nullValue,
    attachableId: !_.isNil(attachableId) ? attachableId : nullValue,
    attachableType: !_.isNil(attachableType) ? attachableType : nullValue,
  };

  if (!isAllowNilValue) {
    return _.pickBy(parsed, v => !_.isNil(v));
  }

  return parsed;
};
