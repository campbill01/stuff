import os
import re
import shutil
from ConfigParser import SafeConfigParser

import boto3


class Connection:
    # will need list, put
    def __init__(self):
        pass

    def get_dir(self,dir):
        pass

    def set_dir(self):
        pass

    def list(self):
        pass

    def put(self):
        pass

class local(Connection):
    def __init__(self,dir=None):
        if dir == None:
            config = SafeConfigParser()
            config.read('config.ini')
            self.directory  = config.get('main', 'DEST_DIR')
        else:
            self.directory = dir

    def __str__(self):
        return self.directory

    def to_string(self):
        return self.directory

    def get_dir(self,dir):
        if not os.path.exists(self.directory + '/' + dir):
            return False
        return True

    def set_dir(self,dir):
        self.directory = dir

    def make_dirs(self,dir):
        os.makedirs(self.directory + '/' + dir)

    def list(self):
        files = []
        for file in os.listdir(self.directory):
            if re.match('.*\.(avi|jpg|mov|mod)',file,re.IGNORECASE):
                filepath=self.directory + "/" + file
                files.append(filepath)
        return files

    def put(self,file):
       prefix = file.replace('/','\\')
       shutil.copyfile(file, self.directory + '\\' + prefix[3:])

class s3(Connection):
    def __init__(self,dir=None):
        # sets bucket info,credentials
        config = SafeConfigParser()
        config.read('config.ini')
        aws_region = config.get('main', 'REGION')
        self.bucket = config.get('main','BUCKET')
        self.client = boto3.client('s3', aws_access_key_id = config.get('main', 'ACCESS_KEY'),
                              aws_secret_access_key=config.get('main', 'SECRET_KEY'),
                              )

    def __str__(self):
        return self.bucket

    def to_string(self):
        return self.bucket

    def list(self):
        # may require pagenation
        pass

    def put(self,file,dest=None):
        up_file = file
        if ':' in file:
            up_file = file[3:]
        up_file = up_file.replace('\\','/')
        self.client.upload_file(file, self.bucket, up_file)

    def make_dirs(self,dirs):
        # s3 creates dir automatically if / is used
        return True
