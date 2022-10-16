import os
import datetime
from typing import Dict

from dotenv import load_dotenv
from boto3.session import Session
from boto3 import resource


class S3:
    load_dotenv()
    bucket = os.getenv("S3_BUCKET")
    access_key = os.getenv("AWS_ACCESS_KEY")
    secret_key = os.getenv("AWS_SECRET_KEY")
    directory = os.path.join("app", "files")

    def resource(self):
        return resource(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    def session(self):
        return Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        ).client('s3')

    def upload(self, file):
        self.session().upload_fileobj(
            Fileobj=file.file,
            Bucket=self.bucket,
            Key=file.filename,
        )

    def download(self, filename: str):
        self.session().download_file(
            Bucket=self.bucket,
            Key=filename,
            Filename=f"{self.directory}/{filename}",
        )

    def delete(self, filename):
        self.session().delete_object(
            Bucket=self.bucket,
            Key=filename,
        )
