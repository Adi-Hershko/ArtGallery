import boto3
from botocore.client import BaseClient

from app.config.config import s3_config


def get_s3_client() -> BaseClient:
    if s3_config.endpoint_url is not None:
        return boto3.client(
            's3',
            aws_access_key_id=s3_config.access_key,
            aws_secret_access_key=s3_config.secret_access_key,
            endpoint_url=s3_config.endpoint_url
        )
    else:
        return boto3.client(
            's3',
            aws_access_key_id=s3_config.access_key,
            aws_secret_access_key=s3_config.secret_access_key
        )
