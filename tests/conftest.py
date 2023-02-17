import os
import random
import string

import pytest


# pylint: disable=line-too-long
@pytest.fixture(scope='function')
def aws_credentials():
    """ mocked credentials and settings """
    os.environ['AWS_ACCESS_KEY_ID'] = f'ASIA{"".join(random.choices(string.ascii_uppercase + "01234567", k=16))}'
    os.environ['AWS_REGION'] = 'us-east-1'
    os.environ['AWS_SECRET_ACCESS_KEY'] = f'{"".join(random.choices("+/" + string.ascii_uppercase + string.ascii_lowercase + string.digits, k=40))}'
    os.environ['AWS_SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:111111111111:some-topic-name'


@pytest.fixture(scope='function')
def aws_credentials_dict():
    """ mocked credentials as a dictionary """
    return {
        'access_key_id': f'ASIA{"".join(random.choices(string.ascii_uppercase + "01234567", k=16))}',
        'region_name': 'us-east-1',
        'secret_access_key': f'{"".join(random.choices("+/" + string.ascii_uppercase + string.ascii_lowercase + string.digits, k=40))}',
        'sns_topic_arn': 'arn:aws:sns:us-east-1:111111111111:some-topic-name',
    }


@pytest.fixture(scope='function')
def aws_credentials_mock():
    """ mocked credentials for boto3 as a dictionary """
    return {
        'aws_access_key_id': f'ASIA{"".join(random.choices(string.ascii_uppercase + "01234567", k=16))}',
        'region_name': 'us-east-1',
        'aws_secret_access_key': f'{"".join(random.choices("+/" + string.ascii_uppercase + string.ascii_lowercase + string.digits, k=40))}',
    }


@pytest.fixture(scope='function')
def dict_data():
    """ generate a simple dictionary for use in tests """
    return {
        'message': 'this is a test message'
    }
