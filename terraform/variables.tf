variable "environment" {
  description = "The working environment that this infrastructure will be deployed into"
  type        = string
}

variable "organization_name" {
  description = "The name of the Terraform Cloud organization that is used for the backend"
  type        = string
}

variable "public_pgp_key" {
  description = "The public PGP key that we will use to encrypt the AWS IAM Secret Key"
  type        = string
}

variable "region" {
  description = "The name of the AWS region that this infrastructure will be deployed into"
  type        = string
}

variable "workspace_name" {
  description = "The name of the Terraform Cloud workspace that will manage this deployment"
  type        = string
}
