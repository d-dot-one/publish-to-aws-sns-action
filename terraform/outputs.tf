output "github_deployer_access_key_id" {
  value = aws_iam_access_key.github_action.id
}

output "github_deployer_secret_key" {
  value = aws_iam_access_key.github_action.encrypted_secret
}

output "sns_topic_arn" {
  value = "The ARN of the SNS Topic that this GitHub action will publish to"
}
