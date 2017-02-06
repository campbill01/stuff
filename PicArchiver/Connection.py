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

    def list(self):
        path=self.directory + "*.JPEG"
        return glob.glob(path)

    def put(self,files):
        for file in files:
            shutil.copy(file,self.directory)

class s3(Connection):
    def __init__(self,where):
        # will need bucket info,credentials
        pass
