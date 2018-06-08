const _ = require('lodash');
const sharp = require('sharp');

module.exports = async ({
  id,
  meta: _meta,
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

  let meta = _meta;

  if (!_.isNil(content) && _.startsWith(type, 'image')) {
    meta = await sharp(content).metadata();
    meta = _.pick(meta, ['width', 'height', 'format']);
    meta = JSON.stringify(meta);
  }

  const parsed = {
    id,
    meta: !_.isNil(meta) ? meta : nullValue,
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
