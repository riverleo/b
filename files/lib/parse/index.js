import _ from 'lodash';

export default ({
  id,
  content,
  filename,
  contentType,
  attachableId,
  attachableType,
}, isAllowNilValue, nullValue = null) => {
  const parsed = {
    id,
    name: !_.isNil(filename) ? filename : nullValue,
    type: !_.isNil(contentType) ? contentType : nullValue,
    bytes: !_.isNil(content) ? content.byteLength : nullValue,
    attachableId: !_.isNil(attachableId) ? attachableId : nullValue,
    attachableType: !_.isNil(attachableType) ? attachableType : nullValue,
  };

  if (!isAllowNilValue) {
    return _.pickBy(parsed, v => !_.isNil(v));
  }

  return parsed;
};
