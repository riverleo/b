import _ from 'lodash';

export const newError = (message, code) => {
  const e = new Error(message);
  e.code = code;

  return e;
};

export const parseSQLError = error => ({
  code: error.code,
  message: error.sqlMessage || error.message,
});

export const parseTranslation = ({ body, lcid }, isAllowNilValue, nullValue = null) => {
  const parsed = {
    body: !_.isNil(body) ? String(body) : nullValue,
    lcid: !_.isNil(lcid) ? String(lcid) : nullValue,
  };

  if (!isAllowNilValue) {
    return _.pickBy(parsed, v => !_.isNil(v));
  }

  return parsed;
};

export default (translations, isAllowNilValue, nullValue = null) => {
  const { key, messageId } = _.first(translations) || {};

  const parsed = {
    id: !_.isNil(messageId) ? Number(messageId) : nullValue,
    key: !_.isNil(key) ? String(key) : nullValue,
    translations: _.map(translations, t => parseTranslation(t, isAllowNilValue, nullValue)),
  };

  if (!isAllowNilValue) {
    return _.pickBy(parsed, v => !_.isNil(v));
  }

  return parsed;
};
