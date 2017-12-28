// ANY

resource "aws_api_gateway_resource" "API_Content" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_rest_api.API.root_resource_id}"
  path_part   = "contents"
}

resource "aws_api_gateway_method" "API_ContentMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_resource.API_Content.id}"
  http_method      = "ANY"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "API_Content_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_Content.id}"
  http_method = "${aws_api_gateway_method.API_ContentMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_ContentIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_Content.id}"
  http_method             = "${aws_api_gateway_method.API_ContentMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:v1_dev_contents/invocations"
}

resource "aws_lambda_permission" "API_ContentPermission" {
  statement_id  = "ContentLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "v1_dev_contents"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*${aws_api_gateway_resource.API_Content.path}"
}

// BY ID

resource "aws_api_gateway_resource" "API_ContentById" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_resource.API_Content.id}"
  path_part   = "{id}"
}

resource "aws_api_gateway_method" "API_ContentByIdMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_resource.API_ContentById.id}"
  http_method      = "ANY"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "API_ContentById_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_ContentById.id}"
  http_method = "${aws_api_gateway_method.API_ContentByIdMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_ContentByIdIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_ContentById.id}"
  http_method             = "${aws_api_gateway_method.API_ContentByIdMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:v1_dev_contents/invocations"
}

resource "aws_lambda_permission" "API_ContentByIdPermission" {
  statement_id  = "ContentByIdLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "v1_dev_contents"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*${aws_api_gateway_resource.API_Content.path}/*"
}
