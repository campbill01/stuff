from ConfigParser import SafeConfigParser
import Connection
from PicFile import PicFile
import re
import os

def load_config():
    # loads settings from ini file
    config = SafeConfigParser()
    config.read('config.ini')
    hash_file = config.get('main','HASH_FILE')
    source_dir = config.get('main','SOURCE_DIR')
    dest_dir = config.get('main','DEST_DIR')
    bucket = config.get('main', 'BUCKET')
    return hash_file,source_dir,dest_dir,bucket


# open hashfile if it exists, create if it doesn't, or close if requested
def manage_hashfile(filename,action=open,hashfile=None):
    if action == "close":
        hashfile.close()
        return
    append_write = 'a+'
    hashfile = open(filename, append_write)
    return hashfile


def make_dirs(dir,destinations):
    for destination in destinations:
        if not destination.get_dir(dir[3:]):
            destination.make_dirs(dir[3:])


# create hash file
def create_hashes(list):
    obj_list=[]
    for item in list:
        file_obj = PicFile(item)
        file_obj.set_hash()
        obj_list.append(file_obj)
    return obj_list


def list_files(directory):
    files = []
    for file in os.listdir(directory):
        if re.match('.*\.(avi|jpg|mov|mod)', file, re.IGNORECASE):
            filepath = directory + "/" + file
            files.append(filepath)
    return files


def upload_files(list,hashfile,destinations):
    for file in list:
        name = file.get_filename()
        hash = file.get_hash()
        found = False
        hashfile.seek(0, 0)
        for line in hashfile:
            if hash == line.split()[0]:
                found=True
                break
        if not found:
            for destination in destinations:
                destination.put(name)
                add_hashes(name,hashfile,hash)


def add_hashes(pic,hashfile,hash):
    hashfile.seek(0, 2)
    line=hash + " " + pic + "\n"
    hashfile.write(line)


if __name__ == "__main__":
    hash_file,source_dir,dest_dir,bucket=load_config()
    hashfile = manage_hashfile(hash_file,'open')
    source_dirs = [x[0] for x in os.walk(source_dir)]
    dest1 = Connection.s3()
    dest2 = Connection.local()
    destinations=[dest1,dest2]
    for dir in source_dirs:
        make_dirs(dir,destinations)
    # list files
        filenames = list_files(dir)
    # select files
        files = create_hashes(filenames)
    # copy files
        upload_files(files,hashfile,destinations)
    manage_hashfile(hash_file,'close',hashfile)

