# tfsec:ignore:aws-lambda-enable-tracing
resource "aws_lambda_function" "github_action" {
  function_name = local.resource_name
  role          = aws_iam_role.github_action.arn
}
