import boto3

# Endpoint URL
endpoint_url = 'https://precioux-cc-p1.s3.ir-thr-at1.arvanstorage.ir'

# Access key ID and secret access key
access_key = 'YOUR_ACCESS_KEY'
secret_key = 'YOUR_SECRET_KEY'

# Bucket name
bucket_name = 'YOUR_BUCKET_NAME'

# Connect to S3
s3_resource = boto3.resource(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# Get a reference to the bucket
bucket = s3_resource.Bucket(bucket_name)

# List objects in the bucket
for obj in bucket.objects.all():
    print(obj.key)

# Upload a file to the bucket
with open('example.txt', 'rb') as f:
    bucket.put_object(Key='example.txt', Body=f)

# Download a file from the bucket
bucket.download_file('example.txt', 'downloaded.txt')

# Delete a file from the bucket
bucket.Object('example.txt').delete()
