from configparser import ConfigParser
import Connection
from PicFile import PicFile
import re
import os

class Archiver:
    def __init__(self):
        self.hash_file, self.source_dir, self.dest_dir, self.dest_type, self.bucket = self.load_config
        self.hashfile_handle = self.manage_hashfile(open)
        self.dir_list = self.get_dirs()
        self.file_list = self.list_files()
        self.picfiles = self.create_hashes()

    def get_dirs(self):
        return [x[0] for x in os.walk(self.source_dir)]

    @property
    def load_config(self):
        # loads settings from ini file
        config = ConfigParser()
        config.read('config.ini')
        hash_file = config.get('main','HASH_FILE')
        source_dir = config.get('main','SOURCE_DIR')
        dest_type = config.get('main','DEST_TYPE')
        if dest_type == 's3':
            dest_dir = Connection.s3()
        else:
            dest_dir = Connection.local(config.get('main','DEST_DIR'))
        bucket = config.get('main', 'BUCKET')
        return hash_file, source_dir, dest_dir, dest_type, bucket

    # open hashfile if it exists, create if it doesn't, or close if requested
    def manage_hashfile(self, action=open):
        if action == "close":
            self.hashfile_handle.close()
            return
        append_write = 'a+'
        hashfile_handle = open(self.hash_file, append_write)
        return hashfile_handle

    def make_dirs(self):
        for directory in self.dir_list:
            if not self.dest_dir.get_dir(directory[3:]):
                # wut?
                #self.dest_dir.make_dirs(directory[3:])
                os.mkdir(self.dest_dir + directory)

    # create hash file
    def create_hashes(self):
        obj_list = []
        for item in self.file_list:
            file_obj = PicFile(item)
            file_obj.set_hash()
            obj_list.append(file_obj)
        return obj_list

    def list_files(self):
        files = []
        for directory in self.dir_list:
            for file in os.listdir(directory):
                if re.match('.*\.(avi|jpg|mov|mod)', file, re.IGNORECASE):
                    filepath = directory + "/" + file
                    files.append(filepath)
        return files

    def upload_files(self):
        for file in self.picfiles:
            name = file.get_filename()
            hash_value = file.get_hash()
            found = False
            self.hashfile_handle.seek(0, 0)
            for line in self.hashfile_handle:
                if hash_value == line.split()[0]:
                    found = True
                    break
            if not found:
                self.dest_dir.put(name)
                self.add_hashes(name, hash_value)

    def add_hashes(self, name, hash_value):
        self.hashfile_handle.seek(0, 2)
        line=hash_value + " " + name + "\n"
        self.hashfile_handle.write(line)


if __name__ == "__main__":
    pic_archive = Archiver()
    pic_archive.upload_files()
    # need to hash dest_dir before upload
    # method to look for dupes
    # error handling
    # call from desktop
    # how to setup destinations /type
    #dest1 = Connection.s3()
    #dest2 = Connection.local()
    pic_archive.manage_hashfile('close')

