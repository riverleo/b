import _ from 'lodash';

export const newError = (message, code) => {
  const e = new Error(message);
  e.code = code;

  return e;
};

export const parseSQLError = error => ({
  code: error.code,
  message: error.sqlMessage,
});

export default ({
  active,
  country,
  language,
  ...props
}, isAllowNilValue, nullValue = null) => {
  const parsed = {
    lcid: `${_.toLower(language)}-${_.toUpper(country)}`,
    active: !_.isNil(active) ? Boolean(active) : nullValue,
    country: !_.isNil(country) ? String(country) : nullValue,
    language: !_.isNil(language) ? String(language) : nullValue,
    ...props,
  };

  if (!isAllowNilValue) {
    return _.pickBy(parsed, v => !_.isNil(v));
  }

  return parsed;
};
