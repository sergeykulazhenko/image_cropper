import os.path
import random

import boto3
from pprint import pprint
from botocore.exceptions import ClientError
from os import path
import random
import diskcache as dc
import tempfile

def list_w_prefix(bucket_name, prefix):
    w_prefix_objects = []
    client = boto3.client('s3')

    paginator = client.get_paginator('list_objects')
    operation_parameters = {
        'Bucket': bucket_name,
        'Prefix': prefix
    }
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        for item in page.get('Contents', []):
            filename = item['Key']
            if filename.endswith('.jpg'):
                w_prefix_objects.append(
                    path.join(
                        path.split(filename)[0].replace(prefix, ''),
                        path.split(filename)[1]
                    )[1:]
                )

    return w_prefix_objects


def download_file(file_name, bucket):
    s3 = boto3.client('s3')
    tempdir = tempfile.gettempdir()
    local_file = os.path.join(
            tempdir,
            os.path.split(file_name)[1]
        )
    with open(
        local_file,
        'wb'
    ) as f:
        s3.download_fileobj(bucket, os.path.join('/original/', file_name), f)

    return local_file


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return False
    return True


def random_uncroped_filename(bucket):
    cache = dc.Cache('tmp1')

    if 'original' in cache:
        originals = cache['original']
    else:
        originals = list_w_prefix(bucket, 'original')

    if 'croped' in cache:
        croped = cache['croped']
    else:
        croped = list_w_prefix(bucket, 'croped')

    objects_to_process = set(originals) - set(croped)
    return random.choice(list(objects_to_process))

if __name__ == "__main__":
    s3_img = os.path.join(
        '/original/',
        random_uncroped_filename('kulazhenko-image-cropper')
    )

    pprint(s3_img)