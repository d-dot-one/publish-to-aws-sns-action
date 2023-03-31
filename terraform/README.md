# Publish to AWS SNS Terraform

This directory contains a set of Terraform files that can be used to build the infrastructure related to this GitHub action. These files assume that you are using Terraform Cloud, but can support any backend configuration that you may have. You simply need to modify the `backend.tf` file to suit your needs. These files are meant to create infrastructure in a single AWS account, but this could easily be extended to multiple AWS accounts using a provider alias and a few more Terraform resources.

Look for any usage of `# todo`, since you will need to make changes according to your own environment and Lambda at these places.

## Usage

```shell
terraform init
terraform apply
```
