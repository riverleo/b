resource "aws_api_gateway_rest_api" "API" {
  name        = "Static"
  description = "static.scdc.co"
  binary_media_types = [
    "*/*",
    "image/*",
    "audio/*",
    "video/*",
    "application/*",
  ]
}

// Deployment

resource "aws_api_gateway_deployment" "API_Deployment" {
  depends_on        = [
    "aws_api_gateway_integration.API_UploadIntegration",
    "aws_api_gateway_integration.API_TransformIntegration",
  ]
  rest_api_id       = "${aws_api_gateway_rest_api.API.id}"
  stage_name        = "prod"
  description       = "Deployed at ${timestamp()}"
  stage_description = "Deployed at ${timestamp()}"

  lifecycle {
    create_before_destroy = true
  }
}
