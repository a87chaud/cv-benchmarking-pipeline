import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv
from app.services.s3_client import get_s3_client
class S3Service:
    def __init__(self):
        load_dotenv()
        self.s3_client = get_s3_client()
        self.bucket = os.getenv('USER_UPLOAD_BUCKET')

    def create_multipart_upload(self, key: str) -> str:
        """Starts the upload process and returns an UploadId."""
        response = self.s3_client.create_multipart_upload(
            Bucket=self.bucket,
            Key=key
        )
        return response['UploadId']

    def generate_part_url(self, key: str, upload_id: str, part_number: int):
        """Generates a pre-signed URL for a specific chunk/part."""
        url = self.s3_client.generate_presigned_url(
            ClientMethod="upload_part",
            Params={
                "Bucket": self.bucket,
                "Key": key,
                "UploadId": upload_id,
                "PartNumber": part_number
            },
            ExpiresIn=3600
        )
        return {
            "partNumber": part_number,
            "url": url
        }

    def complete_multipart_upload(self, key: str, upload_id: str, parts: list):
        """
        Finalizes the upload by joining all parts.
        'parts' should be: [{'PartNumber': 1, 'ETag': '...'}, ...]
        """
        return self.s3_client.complete_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )

    def abort_multipart_upload(self, key: str, upload_id: str):
        """Call this if the frontend catches an error to clean up S3 storage."""
        self.s3_client.abort_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id
        )