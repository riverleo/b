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
  body,
  active,
  component,
  ...props
}, isAllowNilValue, nullValue = null) => {
  const parsed = {
    body: !_.isNil(body) ? String(body) : nullValue,
    active: !_.isNil(active) ? Boolean(active) : nullValue,
    component: !_.isNil(component) ? String(component) : nullValue,
    ...props,
  };

  if (!isAllowNilValue) {
    return _.pickBy(parsed, v => !_.isNil(v));
  }

  return parsed;
};
