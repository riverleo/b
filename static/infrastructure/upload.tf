// POST

resource "aws_api_gateway_method" "API_UploadMethod" {
  rest_api_id   = "${aws_api_gateway_rest_api.API.id}"
  resource_id   = "${aws_api_gateway_rest_api.API.root_resource_id}"
  http_method   = "ANY"
  authorization = "NONE"
  request_parameters = {
    "method.request.header.Content-Type" = true,
  }
}

resource "aws_api_gateway_method_response" "API_Upload_200" {
  rest_api_id = "${aws_api_gateway_rest_api.API.id}"
  resource_id = "${aws_api_gateway_rest_api.API.root_resource_id}"
  http_method = "${aws_api_gateway_method.API_UploadMethod.http_method}"
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
  }
}

resource "aws_api_gateway_integration" "API_UploadIntegration" {
  rest_api_id             = "${aws_api_gateway_rest_api.API.id}"
  resource_id             = "${aws_api_gateway_rest_api.API.root_resource_id}"
  http_method             = "${aws_api_gateway_method.API_UploadMethod.http_method}"
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/${var.lambda_version}/functions/arn:aws:lambda:${var.aws_region}:${var.account_id}:function:static_upload/invocations"
}

resource "aws_lambda_permission" "API_UploadPermission" {
  statement_id  = "UploadLambdaPermission"
  action        = "lambda:InvokeFunction"
  function_name = "static_upload"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.API.id}/*/*"
}
