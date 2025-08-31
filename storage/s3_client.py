import os
import boto3
from botocore.config import Config

def get_s3_client():
    endpoint = os.environ["IDRIVE_ENDPOINT"]
    access_key = os.environ["IDRIVE_ACCESS_KEY"]
    secret_key = os.environ["IDRIVE_SECRET_KEY"]

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4")
    )

def get_users_bucket():
    return os.environ["IDRIVE_BUCKET_USERS"]
