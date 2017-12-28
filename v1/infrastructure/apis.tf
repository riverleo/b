resource "aws_api_gateway_rest_api" "API" {
  name        = "V1 (DEV)"
  description = "scdc api for development"
}

// Deployment

resource "aws_api_gateway_deployment" "API_Deployment" {
  depends_on        = [
    "aws_api_gateway_integration.API_UserIntegration",
    "aws_api_gateway_integration.API_UserByIdIntegration",
  ]
  rest_api_id       = "${aws_api_gateway_rest_api.API.id}"
  stage_name        = "dev"
  description       = "Deployed at ${timestamp()}"
  stage_description = "Deployed at ${timestamp()}"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_api_key" "API_Key" {
  name         = "InApp"
  description  = "API Key for internal applications (non-customer)"
}

resource "aws_api_gateway_usage_plan" "API_UsagePlan" {
  name         = "InApp"
  description  = "Usage plan for internal applications (non-customer)"

  api_stages {
    api_id = "${aws_api_gateway_rest_api.API.id}"
    stage  = "${aws_api_gateway_deployment.API_Deployment.stage_name}"
  }
}

resource "aws_api_gateway_usage_plan_key" "API_UsagePlanKey" {
  key_id        = "${aws_api_gateway_api_key.API_Key.id}"
  key_type      = "API_KEY"
  usage_plan_id = "${aws_api_gateway_usage_plan.API_UsagePlan.id}"
}
