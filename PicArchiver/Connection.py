import glob
import shutil
import re
from os import listdir

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
        #path=self.directory + "*.JPG"
        #return glob.glob(path)



    def put(self,file):
       # print file,self.directory
        shutil.copy(file,self.directory)

class s3(Connection):
    def __init__(self,where):
        # will need bucket info,credentials
        pass
