resource "aws_apigatewayv2_api" "main" {
  name          = "main"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "test" {
  api_id = aws_apigatewayv2_api.main.id

  name        = "${var.env_name}"
  #name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main_api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_cloudwatch_log_group" "main_api_gw" {
  name = "/aws/api-gw/${aws_apigatewayv2_api.main.name}"

  retention_in_days = 5
}

resource "aws_apigatewayv2_integration" "lambda_handler" {
  api_id = aws_apigatewayv2_api.main.id
  integration_method   = "POST"
  integration_type = "AWS_PROXY"
  passthrough_behavior = "WHEN_NO_MATCH"
  integration_uri  = "arn:aws:lambda:eu-west-2:355633558229:function:${var.image_name}-${var.env_name}"
}

resource "aws_apigatewayv2_route" "post_handler" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /{proxy+}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_handler.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = "${var.image_name}-${var.env_name}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}