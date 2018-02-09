from hashlib import md5


class PicFile:

    def __init__(self, file_name):
        self.file_name = file_name
        self.hash_value = 0

    def set_hash(self):
        hash = md5()
        with open(self.file_name, "rb") as f:
            for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
                hash.update(chunk)
        self.hash_value = hash.hexdigest()

    def get_hash(self):
        return self.hash_value

    def set_filename(self,name):
        self.file_name = name

    def get_filename(self):
        return self.file_name






