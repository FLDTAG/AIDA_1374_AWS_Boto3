import boto3
import os


def create_bucket(bucket_name):
  bucket = s3.Bucket(bucket_name)
  if not bucket in s3.buckets.all():
    response = bucket.create(CreateBucketConfiguration={
        'LocationConstraint': session.region_name
        }
        )
  else:
    response = f'Bucket \'{bucket_name}\' already exists.'
  print('RESPONSE:')
  print(response)
  print()
  return bucket


def file_upload(bucket, source_dir, target_dir):
    #uploading ALL files from source_dir
    for file in os.listdir(source_dir):
        bucket.upload_file(Filename=source_dir+'/'+file, Key=target_dir+'/'+file)
        response = bucket.meta.client.head_object(Bucket=bucket.name, Key=target_dir+'/'+file)
        print('Uploaded '+file+' to '+target_dir+'/'+file)
        print('RESPONSE:')
        print(response)
        print()


def file_download(bucket, source_path, target_path):
    bucket.download_file(source_path, target_path)
    print('Downloaded ' + source_path + ' to ' + target_path)
    print()


def file_delete(bucket, file_path):
    response = bucket.delete_objects(Delete={'Objects': [{'Key': file_path}]})
    print('Deleted ' + file_path)
    print('RESPONSE:')
    print(response)
    print()


session = boto3.Session(aws_access_key_id="SECRET", aws_secret_access_key="SECRET", region_name="eu-central-1")
s3 = session.resource("s3")

my_bucket = create_bucket('falks-bucket')
file_upload(my_bucket, 'files', 'files')
file_download(my_bucket, 'files/sheep-unsplash.jpg', 'files/sheep-unsplash_dl.jpg')
file_delete(my_bucket, 'files/sheep-unsplash.jpg')
