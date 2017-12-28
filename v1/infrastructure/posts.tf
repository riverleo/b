// ANY

resource "aws_api_gateway_resource" "API_Post" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_rest_api.API.root_resource_id}"
  path_part   = "posts"
}

resource "aws_api_gateway_method" "API_PostMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_resource.API_Post.id}"
  http_method      = "ANY"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "API_Post_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_Post.id}"
  http_method = "${aws_api_gateway_method.API_PostMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_PostIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_Post.id}"
  http_method             = "${aws_api_gateway_method.API_PostMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:v1_dev_posts/invocations"
}

resource "aws_lambda_permission" "API_PostPermission" {
  statement_id  = "PostLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "v1_dev_posts"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*${aws_api_gateway_resource.API_Post.path}"
}

// BY ID

resource "aws_api_gateway_resource" "API_PostById" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_resource.API_Post.id}"
  path_part   = "{id}"
}

resource "aws_api_gateway_method" "API_PostByIdMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_resource.API_PostById.id}"
  http_method      = "ANY"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "API_PostById_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_PostById.id}"
  http_method = "${aws_api_gateway_method.API_PostByIdMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_PostByIdIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_PostById.id}"
  http_method             = "${aws_api_gateway_method.API_PostByIdMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:v1_dev_posts/invocations"
}

resource "aws_lambda_permission" "API_PostByIdPermission" {
  statement_id  = "PostByIdLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "v1_dev_posts"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*${aws_api_gateway_resource.API_Post.path}/*"
}
