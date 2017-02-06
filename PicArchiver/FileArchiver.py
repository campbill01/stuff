import Connection
import PicFile
import os.path

#default settings
#hash file
hash_file='.\hashfile'
# source location
source_dir='d:\\test\\'
# destination
dest_dir='e:\\test\\'
# first run ?
def setup():
    #not implemented
    pass

# create hash file
def create_hashes(list):
    obj_list=[]
    for item in list:
        file_obj = PicFile(item)
        file_obj.set_hash()
        obj_list.append(file_obj)
    return obj_list

def get_settings():
    # read settings from file (configparser)
    # not implemented
    pass

def list_files(connection):
    # should take a connection and use it's methods to access/enumerate files
    # should theoretically be blind to the actual implementation
    return connection.list()

def upload_files(list):
    for file in list:
        destination.put(file.get_filename())

def add_hashfile(pics):
    #create if not exist
    #or seek end of file
     if os.path.isfile(hash_file):
        open(hash_file, "rb") as f:
        f.seek(0,2)
     for file in pics:
         hash=file.get_hash()
         filename=file.get_filename()
         f.write(hash + ":" + filename)




if __name__ == "__main__":
    # make connections
    source = Connection.local(source_dir)
    destination = Connection.local(dest_dir)
    # list files
    filenames = list_files(source)
    # select files
    # initially will be all files
    files = create_hashes(filenames)
     # copy files
    upload_files(files)
    # update hash file
    add_hashes(files)

