import sys
import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

domain = 'https://c525438.parspack.net'
bucketName = 'c525438'
accessKey = 'aBiXEYr6whnbrfxc'
secretKey = 'Z4rDp16QyX6q6lQLdRDZKZvWlGzjepty'

try:
    s3_resource = boto3.resource(
        's3',
        endpoint_url=domain,
        aws_access_key_id=accessKey,
        aws_secret_access_key=secretKey
    )
except Exception as exc:
    logging.info(exc)
else:

    bucket = s3_resource.Bucket(bucketName)


def find_file(id):
    idstr = str(id)
    for obj in bucket.objects.all():
        filename = str(obj.key)
        print(f'Checking file {filename}...')
        if idstr in filename:
            print('Found!')
            return filename
    print(f'File with id {idstr} not found!')
    return None


def list_files():
    for obj in bucket.objects.all():
        logging.info(f"object_name: {obj.key}, last_modified: {obj.last_modified}")



def upload_file(file, object_name):
    contents = file.file.read()
    bucket.put_object(
        ACL='private',
        Body=contents,
        Key=object_name
    )
    print(f'INFO:     File-{object_name} uploaded successfully')


def get_url(filename):
    filename = str(filename).split("'")[1]
    url = f"{domain}/{bucketName}/{filename}"
    return url


def download_file(object_name, download_path):
    bucket.download_file(
        object_name,
        download_path
    )


def delete_file(object_name):
    object_name = 'parspack.png'
    object = bucket.Object(object_name)
    object.delete()

def get_file_content(object_name):
    try:
        obj = bucket.Object(object_name)
        response = obj.get()
        file_content = response['Body'].read().decode('utf-8')
        return file_content
    except ClientError as e:
        logging.error(e)
        return None
