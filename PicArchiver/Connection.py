import glob
import shutil

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


    def list(self):
        path=self.directory + "*.JPG"
        return glob.glob(path)

    def put(self,file):
       # print file,self.directory
        shutil.copy(file,self.directory)

class s3(Connection):
    def __init__(self,where):
        # will need bucket info,credentials
        pass
