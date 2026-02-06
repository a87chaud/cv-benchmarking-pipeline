from typing import Self
from botocore.config import Config
from dotenv import load_dotenv
import boto3
import os

load_dotenv()

_s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2",
    config=Config(
        signature_version="s3v4",
        region_name="us-east-2",
        s3={"addressing_style": "virtual"}
    )
)

def get_s3_client():
    return _s3_client
