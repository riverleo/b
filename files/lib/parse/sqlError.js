export default error => ({
  code: error.code,
  message: error.sqlMessage || error.message,
});
