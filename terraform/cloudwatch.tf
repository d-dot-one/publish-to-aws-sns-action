resource "aws_cloudwatch_log_group" "github_action" {
  name              = "/aws/lambda/${aws_lambda_function.github_action.function_name}"
  kms_key_id        = aws_kms_key.github_action.key_id
  retention_in_days = 30

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_cloudwatch_log_stream" "github_action" {
  log_group_name = aws_cloudwatch_log_group.github_action.name
  name           = local.resource_name
}

resource "aws_iam_policy" "github_action_cloudwatch_logging" {
  description = "This policy grants a Lambda function role permissions to log to AWS Cloudwatch"
  name        = "lambda-function-logging-policy"
  policy      = data.aws_iam_policy_document.github_action_cloudwatch.json
}

data "aws_iam_policy_document" "github_action_cloudwatch" {
  statement {
    actions   = ["logs:PutLogEvents"]
    effect    = "Allow"
    resources = [aws_cloudwatch_log_stream.github_action.arn]
    sid       = "AllowCloudwatchLogging"
  }
}

resource "aws_iam_role_policy_attachment" "github_action_cloudwatch_logging" {
  role       = aws_iam_role.github_action.id
  policy_arn = aws_iam_policy.github_action_cloudwatch_logging.arn
}
