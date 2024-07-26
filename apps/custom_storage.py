from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None):
        url = super().url(name, parameters, expire)
        if settings.EXTERNAL_AWS_S3_ENDPOINT_URL:
            internal_endpoint = settings.AWS_S3_ENDPOINT_URL
            external_endpoint = settings.EXTERNAL_AWS_S3_ENDPOINT_URL
            if internal_endpoint in url:
                url = url.replace(internal_endpoint, external_endpoint)
        return url
