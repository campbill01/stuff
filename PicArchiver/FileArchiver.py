import Connection
from PicFile import PicFile
import os
#default settings
#hash file
hash_file='.\hashfile'
# source location
source_dir='d:\\test'
# destination
dest_dir='e:\\'
# first run ?
def setup():
    #not implemented
    pass

# open hashfile if it exists, create if it doesn't, or close if requested
def manage_hashfile(filename,action=open,hashfile=None):
    if action == "close":
        hashfile.close()
        return
    append_write = 'a+'
    hashfile = open(filename, append_write)
    #hashfile.seek(0, 2)
    return hashfile

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

def upload_files(list,hashfile):
    for file in list:
        name = file.get_filename()
        hash = file.get_hash()
        found = False
        for line in hashfile:
           # print line.split()[0]
            if hash == line.split()[0]:
                found=True
                break
        if not found:
            destination.put(name)
            add_hashes(name,hashfile,hash)

def add_hashes(pic,hashfile,hash):
    line=hash + " " + pic + "\n"
    hashfile.write(line)



if __name__ == "__main__":
    hashfile = manage_hashfile(hash_file,'open')
    # this needs to be a base dir instead of an absolute source
    # perhaps traverse directories and get list and then call metchod/functions on each ?
    #  [x[0] for x in os.walk('e:\\camera')]
    # or
    # d='.'
    # filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d))
    source_dirs = [x[0] for x in os.walk(source_dir)]
    for dir in source_dirs:
        source = Connection.local(dir)
        destination = Connection.local(dest_dir + dir[2:])
        if not os.path.exists(destination.to_string()):
            os.makedirs(destination.to_string())
    # list files
        filenames = list_files(source)
    # select files
        files = create_hashes(filenames)
    # copy files
        upload_files(files,hashfile)
    # update hash file
    manage_hashfile(hash_file,'close',hashfile)

