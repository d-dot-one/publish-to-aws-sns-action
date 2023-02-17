# pylint: disable=protected-access
import json
import os
import random
import string

import boto3  # type: ignore
import pytest
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from moto import mock_sns

from action import publish_to_sns
from action.publish_to_sns import SnsConnection


class TestPublishToSns:
    """ test suite for the publish_to_sns logic """
    @pytest.mark.unit
    @pytest.mark.parametrize(
        'access_key',
        [
            f'ASIA{"".join(random.choices(string.ascii_uppercase + "01234567", k=16))}',
            f'AKIA{"".join(random.choices(string.ascii_uppercase + "01234567", k=16))}',
            f'AROA{"".join(random.choices(string.ascii_uppercase + "01234567", k=16))}',
            f'AIDA{"".join(random.choices(string.ascii_uppercase + "01234567", k=16))}',
        ]
    )
    def test_verify_access_key_id(self, access_key, aws_credentials):
        """ test the access key id validation """
        os.environ['AWS_ACCESS_KEY_ID'] = access_key
        assert SnsConnection()._verify_and_set_access_key_id(access_key_id=access_key) == access_key

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'access_key',
        [
            111111111111,
            {'a': 1, 'b': 2},
            ['a', 'b', 'c'],
            None,
            '',
        ]
    )
    def test_verify_access_key_id_type_error(self, access_key, aws_credentials):
        """ test the access key ID validation for type error handling """
        with pytest.raises(TypeError) as err:
            _ = SnsConnection()._verify_and_set_access_key_id(access_key_id=access_key)

        assert err.type == TypeError

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'access_key',
        [
            f'ASIA{"".join(random.choices(string.ascii_uppercase + "01234567", k=6))}',
            f'AKIA{"".join(random.choices(string.ascii_uppercase + "01234567", k=26))}',
            f'AROA{"".join(random.choices(string.ascii_uppercase + "01234567", k=40))}',
            f'some random string that is just long enough',
        ]
    )
    def test_verify_access_key_id_value_error(self, access_key, aws_credentials):
        """ test the access key ID validation for value error handling """
        with pytest.raises(ValueError) as err:
            _ = SnsConnection()._verify_and_set_access_key_id(access_key_id=access_key)

        assert err.type == ValueError

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'secret_key',
        [
            f'{"".join(random.choices(string.ascii_letters + string.digits, k=40))}',
            f'{"".join(random.choices(string.ascii_letters + string.digits, k=40))}',
            f'{"".join(random.choices(string.ascii_letters + string.digits, k=40))}',
        ]
    )
    def test_verify_secret_access_key(self, secret_key, aws_credentials):
        """ test the secret access key validation """
        os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
        assert SnsConnection()._verify_and_set_secret_access_key(secret_access_key=secret_key) == secret_key

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'secret_key',
        [
            111111111111,
            {'a': 1, 'b': 2},
            ['a', 'b', 'c'],
            None,
            '',  # this should throw a warning log, but otherwise should pass this test
        ]
    )
    def test_verify_secret_access_key_type_error(self, secret_key, aws_credentials):
        """ test the secret access key validation type error handling """
        with pytest.raises(TypeError) as err:
            _ = SnsConnection()._verify_and_set_secret_access_key(secret_access_key=secret_key)

        assert err.type == TypeError

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'secret_key',
        [
            f'{"".join(random.choices(string.ascii_letters + string.digits, k=20))}',
            f'{"".join(random.choices(string.ascii_letters + string.digits, k=39))}',
            f'{"".join(random.choices(string.ascii_letters + string.digits, k=41))}',
            f'{"".join(random.choices(string.ascii_letters + string.digits, k=60))}',
        ]
    )
    def test_verify_secret_access_key_value_error(self, secret_key, aws_credentials):
        """ test the secret access key validation value error handling """
        with pytest.raises(ValueError) as err:
            _ = SnsConnection()._verify_and_set_secret_access_key(secret_access_key=secret_key)

        assert err.type == ValueError

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'region',
        [
            'us-east-1',
            'ap-northeast-2',
            'eu-central-5',
            'us-gov-east-1',
        ]
    )
    def test_verify_region(self, region, aws_credentials):
        """ test the aws region validation """
        os.environ['AWS_REGION'] = region
        assert SnsConnection()._verify_and_set_region(region=region) == region

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'region',
        [
            123457,
            None,
            {'a': 1, 'b': 'something else'},
            [1, 2, 3, 4, 5]
        ]
    )
    def test_verify_region_type_error(self, region, aws_credentials):
        """ test the aws region validation for type error handling """
        with pytest.raises(TypeError) as err:
            os.environ['AWS_REGION'] = region
            _ = SnsConnection()._verify_and_set_region(region=region)

        assert err.type == TypeError

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'region',
        [
            'ca-westeast-1',
            'zz-east-1',
        ]
    )
    def test_verify_region_value_error(self, region, aws_credentials):
        """ test the aws region validation for value error handling """
        os.environ['AWS_REGION'] = region
        with pytest.raises(ValueError) as err:
            _ = SnsConnection()._verify_and_set_region(region=region)

        assert err.type == ValueError

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'topic_arn',
        ['arn:aws:sns:us-east-1:111111111111:some-name']
    )
    def test_verify_sns_topic_arn(self, topic_arn, aws_credentials):
        """ test the sns topic arn validation """
        os.environ['SNS_TOPIC_ARN'] = topic_arn
        assert SnsConnection()._verify_and_set_sns_topic_arn(topic_arn=topic_arn) == topic_arn

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'topic_arn',
        ['arn:aws:iam:us-east-1:111111111111:some-name']
    )
    def test_verify_sns_topic_arn_value_error(self, topic_arn, aws_credentials):
        """ test the sns topic arn validation for value error handling """
        with pytest.raises(ValueError) as err:
            _ = SnsConnection()._verify_and_set_sns_topic_arn(topic_arn=topic_arn)

        assert err.type == ValueError

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'topic_arn',
        [
            123457,
            None,
            {'a': 1, 'b': 'something else'},
            [1, 2, 3, 4, 5]
        ]
    )
    def test_verify_sns_topic_arn_type_error(self, topic_arn, aws_credentials):
        """ test the sns topic arn validation for type error handling """
        with pytest.raises(TypeError) as err:
            _ = SnsConnection()._verify_and_set_sns_topic_arn(topic_arn=topic_arn)

        assert err.type == TypeError

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'commit_id',
        [
            '508ca9f7f566d70e3cdc100f08cc090b01cdc7c6',
            '647fa0305846508f5c8d753b40108d8fac1d6687',
            '35d1cd161cd6f5e676815db91e622366a0a82892',
        ]
    )
    def test_verify_and_set_github_commit_id(self, commit_id, aws_credentials):
        """ test the GitHub commit ID validation """
        assert SnsConnection()._verify_and_set_github_commit_id(commit_id=commit_id) == commit_id

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'commit_id',
        [
            'somefakehashthatisthecorrectlengthfriend',
            '647fa03058465',
        ]
    )
    def test_verify_and_set_github_commit_id_value_error(self, commit_id, aws_credentials):
        """ test the GitHub commit ID validation for value errors """
        with pytest.raises(ValueError) as err:
            _ = SnsConnection()._verify_and_set_github_commit_id(commit_id=commit_id)

        assert err.type == ValueError

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'commit_id',
        [
            123457,
            None,
            {'a': 1, 'b': 'something else'},
            [1, 2, 3, 4, 5]
        ]
    )
    def test_verify_and_set_github_commit_id_type_error(self, commit_id, aws_credentials):
        """ test the GitHub commit ID validation for type errors """
        with pytest.raises(TypeError) as err:
            _ = SnsConnection()._verify_and_set_github_commit_id(commit_id=commit_id)

        assert err.type == TypeError

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'key, result',
        [
            ('AAAAAAAAAAAAAAAAAAAA', 'AAAA************AAAA'),
            ('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'AAAAAAAA****************************AAAA')
        ]
    )
    def test_obfuscate_key(self, key, result, aws_credentials):
        """ test the key obfuscation """
        assert SnsConnection()._obfuscate_key(key=key) == result

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'key',
        [
            'AAAAAAAAAAAAAAAAAAA',  # 19
            'AAAAAAAAAAAAAAAAAAAAA',  # 21
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',  # 39
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',  # 41
        ]
    )
    def test_obfuscate_key_value_error(self, key, aws_credentials):
        """ test the key obfuscation value error handling """
        with pytest.raises(ValueError) as err:
            _ = SnsConnection()._obfuscate_key(key=key)

        assert err.type == ValueError

    @mock_sns
    @pytest.mark.unit
    def test_create_sns_client(self, aws_credentials_dict):
        """ test the creation of an sns client """
        sns_client = SnsConnection(**aws_credentials_dict)

        assert isinstance(sns_client, publish_to_sns.SnsConnection)

    @mock_sns
    @pytest.mark.unit
    @pytest.mark.exception
    def test_create_sns_client_client_error(self):
        """ test the creation of an sns client error handling """

        sns_client = None

        with pytest.raises(ClientError) as err:
            if not (sns_client and isinstance(sns_client, BaseClient)):
                raise ClientError(error_response={}, operation_name='sns')

        assert err.type == ClientError

    @mock_sns
    @pytest.mark.unit
    def test_publish_sns_message(self, dict_data, aws_credentials_dict):
        """ test the logic to publish to an sns topic """
        sns_client = SnsConnection(**aws_credentials_dict)
        _ = sns_client.client.create_topic(Name='some-topic-name')

        response = sns_client.client.list_topics()

        sns_topic_arn = response.get('Topics', [])[0].get('TopicArn')

        response = sns_client.publish_sns_message(
            dict_data=dict_data,
            sns_topic_arn=sns_topic_arn,
        )

        assert response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200

    @pytest.mark.unit
    @pytest.mark.exception
    @mock_sns
    def test_publish_sns_message_too_big(self, aws_credentials_dict):
        """ test the logic that verifies message size """
        sns_client = SnsConnection(**aws_credentials_dict)
        _ = sns_client.client.create_topic(Name='some-topic-name')

        response = sns_client.client.list_topics()
        sns_topic_arn = response.get('Topics', [])[0].get('TopicArn')

        os.environ['SNS_TOPIC_ARN'] = sns_topic_arn

        big_data = ''.join(['a' for _ in range(0, 333333)])

        big_message = {
            'message': big_data
        }

        with pytest.raises(ValueError) as err:
            _ = sns_client.publish_sns_message(
                dict_data=big_message,
                sns_topic_arn=sns_topic_arn,
            )

        assert err.type == ValueError

    @pytest.mark.unit
    @pytest.mark.exception
    @pytest.mark.parametrize(
        'test_data',
        [
            None,
            'AAAAAAAAAAAAAAAAAAAAA',  # 21
            [1, 2, 3, 4, 5],
            123456,  # 41
        ]
    )
    @mock_sns
    def test_publish_sns_message_type_error(self, test_data, aws_credentials_dict):
        """ test the logic that verifies message type """
        sns_client = SnsConnection(**aws_credentials_dict)
        _ = sns_client.client.create_topic(Name='some-topic-name')

        response = sns_client.client.list_topics()
        sns_topic_arn = response.get('Topics', [])[0].get('TopicArn')

        os.environ['SNS_TOPIC_ARN'] = sns_topic_arn

        with pytest.raises(TypeError) as err:
            _ = sns_client.publish_sns_message(
                dict_data=test_data,
                sns_topic_arn=sns_topic_arn,
            )

        assert err.type == TypeError

    @pytest.mark.unit
    @pytest.mark.exception
    @mock_sns
    def test_publish_sns_message_type_error_json(self, aws_credentials_dict):
        """ test the logic that catches json issues """
        sns_connection = SnsConnection(**aws_credentials_dict)
        with pytest.raises(TypeError) as err:
            json.dumps(sns_connection)

        assert err.type == TypeError
