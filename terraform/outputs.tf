output "github_deployer_access_key_id" {
  value = aws_iam_access_key.github_action.id
}

output "github_deployer_secret_key" {
  value = aws_iam_access_key.github_action.encrypted_secret
}
