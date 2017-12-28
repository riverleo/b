// TRANSFORM

resource "aws_api_gateway_resource" "API_Transform" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  parent_id   = "${aws_api_gateway_rest_api.API.root_resource_id}"
  path_part   = "{key}"
}

resource "aws_api_gateway_method" "API_TransformMethod" {
  rest_api_id   = "${aws_api_gateway_rest_api.API.id}"
  resource_id   = "${aws_api_gateway_resource.API_Transform.id}"
  http_method   = "GET"
  authorization = "NONE"
  request_parameters = {
    "method.request.path.key"                = true,
    "method.request.querystring.s"           = true,
    "method.request.querystring.aspectRatio" = true,
  }
}

resource "aws_api_gateway_method_settings" "API_TransformMethodSettings" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  stage_name = "prod"
  method_path = "${aws_api_gateway_resource.API_Transform.path_part}/${aws_api_gateway_method.API_TransformMethod.http_method}"

  settings {
    caching_enabled = true,
    cache_ttl_in_seconds = 3600,
  }
}

resource "aws_api_gateway_method_response" "API_Transform_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_resource.API_Transform.id}"
  http_method = "${aws_api_gateway_method.API_TransformMethod.http_method}"
  status_code = "200"
}

resource "aws_api_gateway_integration" "API_TransformIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_resource.API_Transform.id}"
  http_method             = "${aws_api_gateway_method.API_TransformMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:static_transform/invocations"
  cache_key_parameters = [
    "method.request.path.key",
    "method.request.querystring.s",
    "method.request.querystring.aspectRatio",
  ]
}

resource "aws_lambda_permission" "API_TransformPermission" {
  statement_id  = "TransformLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "static_transform"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*${aws_api_gateway_resource.API_Transform.path}"
}
