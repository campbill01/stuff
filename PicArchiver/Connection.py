import glob
import shutil
import re
from os import listdir
from ConfigParser import SafeConfigParser
import boto3

class Connection:
    # will need list, put
    def __init__(self):
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


    def list(self):
        files = []
        for file in listdir(self.directory):
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
        self.bucket = where
        aws_region = config.get('main', 'REGION')
        client = boto3.client('s3', aws_access_key_id = config.get('main', 'ACCESS_KEY'),
                              aws_secret_access_key=config.get('main', 'SECRET_KEY'),
                              )

    def __str__(self):
        return self.bucket

    def to_string(self):
        return self.bucket

    def list(self):
        pass

    def put(self,file):
        pass