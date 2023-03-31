# Publish to AWS SNS Topic - GitHub Action
This is a GitHub Action that will publish a JSON message to an AWS SNS Topic. By default, this action will return the
entire GitHub context as the `MESSAGE` for the AWS SNS topic. To send more specific data, update the `MESSAGE`
environment variable that is passed in your `.github/workflows/publish-to-sns.yaml`.

## Environment Variables
The following inputs are required for this GitHub Action to successfully execute. These inputs should be entered in
your GitHub repository settings (**Secrets > Secrets and variables > Actions > Secrets tab**):

| Name                    | Type   | Description                                                |
|-------------------------|--------|------------------------------------------------------------|
| `AWS_ACCESS_KEY_ID`     | string | The access key ID for the AWS IAM user (20 characters)     |
| `AWS_SECRET_ACCESS_KEY` | string | The secret access key for the AWS IAM user (40 characters) |
| `AWS_REGION`            | string | The AWS region where the SNS topic exists                  |
| `AWS_SNS_TOPIC_ARN`     | string | The ARN of the SNS Topic to publish to                     |

## Example Usage
This example shows you a typical use case configuration of `.github/workflows/publish-to-sns.yaml` where the action
will execute when a pull request is opened:

```yaml
name: Publish to AWS SNS Topic

on:
  pull_request:
    types: [opened, reopened, edited, ready_for_review]

env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_REGION: ${{ secrets.AWS_REGION }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  AWS_SNS_TOPIC_ARN: ${{ secrets.SNS_TOPIC_ARN }}
  MESSAGE: ${{ toJSON(github) }}

jobs:
  publish-to-sns:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Publish to AWS SNS Topic
        uses: d-dot-one/publish-to-sns@v1

```

## Message Format
This action publishes a message in the following format to AWS SNS:

```json
{
  "message": "<JSON-formatted message>",
  "commit_id": "<GitHub Commit ID>"
}
```

## Required Permissions
You only need a single permission to be granted to the AWS IAM user that performs this action:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSnSPublishForGitHubAction",
      "Action": [
        "sns:Publish"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:sns:us-east-1:111111111111:some-topic-name"
    }
  ]
}
```

## Terraform
You will find a `terraform` directory in this repository. It contains the infrastructure that you will need for this action to work in your environment. Consult the `README.md` there for more information.

## License
This project is licensed under the [MIT License](LICENSE.md).
