export default (event, context, callback) => callback(null, {
  statusCode: 201,
  body: JSON.stringify(event),
});
