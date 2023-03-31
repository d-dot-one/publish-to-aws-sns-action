resource "aws_sns_topic" "github_action" {
  display_name      = local.resource_name
  fifo_topic        = false
  name              = local.resource_name
  kms_master_key_id = aws_kms_key.github_action.key_id

  tags = {
    Name = local.resource_name
  }
}

resource "aws_sns_topic_policy" "github_action" {
  arn    = aws_sns_topic.github_action.arn
  policy = data.aws_iam_policy_document.github_action.json
}

data "aws_iam_policy_document" "github_action" {
  statement {
    actions = ["sns:Publish"]
    effect  = "Allow"

    principals {
      type        = "AWS"
      identifiers = [aws_iam_user.github_action.arn]
    }

    resources = [aws_sns_topic.github_action.arn]
    sid       = "PublishToSns"
  }
}

resource "aws_sns_topic_subscription" "github_action" {
  topic_arn = aws_sns_topic.github_action.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.github_action.arn
}
