module.exports = (statusCode, message) => {
  const e = new Error(message);

  e.statusCode = statusCode;

  return e;
};
