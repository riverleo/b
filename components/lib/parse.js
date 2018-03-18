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
  style,
  ...props
}, isAllowNilValue, nullValue = null) => {
  const parsed = {
    style: !_.isNil(style) ? String(style) : nullValue,
    ...props,
  };

  if (!isAllowNilValue) {
    return _.pickBy(parsed, v => !_.isNil(v));
  }

  return parsed;
};
