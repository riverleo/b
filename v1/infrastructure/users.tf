// ANY

resource "aws_api_gateway_resource" "API_User" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_rest_api.API.root_resource_id}"
  path_part   = "users"
}

resource "aws_api_gateway_method" "API_UserMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_resource.API_User.id}"
  http_method      = "ANY"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "API_User_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_User.id}"
  http_method = "${aws_api_gateway_method.API_UserMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_UserIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_User.id}"
  http_method             = "${aws_api_gateway_method.API_UserMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:v1_dev_users/invocations"
}

resource "aws_lambda_permission" "API_UserPermission" {
  statement_id  = "UserLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "v1_dev_users"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*${aws_api_gateway_resource.API_User.path}"
}

// GET BY ID

resource "aws_api_gateway_resource" "API_UserById" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_resource.API_User.id}"
  path_part   = "{id}"
}

resource "aws_api_gateway_method" "API_UserByIdMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_resource.API_UserById.id}"
  http_method      = "ANY"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "API_UserById_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_UserById.id}"
  http_method = "${aws_api_gateway_method.API_UserByIdMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_UserByIdIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_UserById.id}"
  http_method             = "${aws_api_gateway_method.API_UserByIdMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:v1_dev_users/invocations"
}

resource "aws_lambda_permission" "API_UserByIdPermission" {
  statement_id  = "UserByIdLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "v1_dev_users"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*${aws_api_gateway_resource.API_User.path}/*"
}
