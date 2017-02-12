import os
import re
import shutil
from ConfigParser import SafeConfigParser

import boto3
import botocore


class Connection:
    # will need list, put
    def __init__(self):
        pass

    def get_dir(self):
        pass

    def set_dir(self):
        pass

    def list(self):
        pass

    def put(self):
        pass

class local(Connection):
    def __init__(self, where):
        # support only top level directories at first
        self.directory = where

    def __str__(self):
        return self.directory

    def to_string(self):
        return self.directory

    def get_dir(self):
        if not os.path.exists(self.directory):
            return False
        return True

    def set_dir(self):
        os.makedirs(self.directory)

    def list(self):
        files = []
        for file in os.listdir(self.directory):
            if re.match('.*\.(avi|jpg|mov|mod)',file,re.IGNORECASE):
                filepath=self.directory + "/" + file
                files.append(filepath)
        return files

    def put(self,file):
       # print file,self.directory
        shutil.copy(file,self.directory)

class s3(Connection):
    def __init__(self,where):
        # sets bucket info,credentials
        config = SafeConfigParser()
        config.read('config.ini')
        path =  where.find('/')
        if path == -1:
            self.bucket = where
            self.dir = '/'
        else:
            bucket=where[0:path]
            self.dir = where[path:]
        self.destination = self.bucket + self.dir
        aws_region = config.get('main', 'REGION')
        self.client = boto3.client('s3', aws_access_key_id = config.get('main', 'ACCESS_KEY'),
                              aws_secret_access_key=config.get('main', 'SECRET_KEY'),
                              )

    def __str__(self):
        return self.destination

    def to_string(self):
        return self.destination

    def list(self):
        # may require pagenation
        pass

    def put(self,file):
        #with open (file, 'rb') as data:
            #this will probably add bucket to path of remote file
        print file
        if self.bucket in file:
            upfile = file[len(self.bucket):]
            #print file
        if ':' in file:
            upfile = file[2:]
        self.client.upload_file(file, self.bucket, upfile)

    def get_dir(self):
        try:
            key=self.client.head_object(Bucket=self.bucket,Key=self.destination)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise
        else:
            return True

    def set_dir(self):
        self.client.put_object(
            Bucket=self.bucket,
            Body='',
            Key=self.destination +'/'
        )