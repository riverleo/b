resource "aws_api_gateway_rest_api" "API" {
  name        = "Link"
  description = "scdc.co"
}

// Deployment

resource "aws_api_gateway_deployment" "API_Deployment" {
  depends_on        = [
    "aws_api_gateway_integration.API_CreateIntegration",
  ]
  rest_api_id       = "${aws_api_gateway_rest_api.API.id}"
  stage_name        = "prod"
  description       = "Deployed at ${timestamp()}"
  stage_description = "Deployed at ${timestamp()}"

  lifecycle {
    create_before_destroy = true
  }
}

// CREATE

resource "aws_api_gateway_method" "API_CreateMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_rest_api.API.root_resource_id}"
  http_method      = "ANY"
  authorization    = "NONE"
}

resource "aws_api_gateway_method_response" "API_Create_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_rest_api.API.root_resource_id}"
  http_method = "${aws_api_gateway_method.API_CreateMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_CreateIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_rest_api.API.root_resource_id}"
  http_method             = "${aws_api_gateway_method.API_CreateMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:link_create/invocations"
}

resource "aws_lambda_permission" "API_CreatePermission" {
  statement_id  = "CreateLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "link_create"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*"
}

// REDIRECT

resource "aws_api_gateway_resource" "API_Redirect" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_rest_api.API.root_resource_id}"
  path_part   = "{key}"
}

resource "aws_api_gateway_method" "API_RedirectMethod" {
  rest_api_id      = "${aws_api_gateway_rest_api.API.id}"
  resource_id      = "${aws_api_gateway_resource.API_Redirect.id}"
  http_method      = "GET"
  authorization    = "NONE"
}

resource "aws_api_gateway_method_response" "API_Redirect_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_Redirect.id}"
  http_method = "${aws_api_gateway_method.API_RedirectMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_RedirectIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_Redirect.id}"
  http_method             = "${aws_api_gateway_method.API_RedirectMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:link_redirect/invocations"
}

resource "aws_lambda_permission" "API_RedirectPermission" {
  statement_id  = "RedirectPermission"
  action        = "lambda:InvokeFunction"
  function_name = "link_redirect"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*"
}
