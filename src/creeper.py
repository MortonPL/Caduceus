import os
from hashlib import md5 as hashlib_md5
from src.file import File, Flags

BUF_SIZE = 65536

class Creeper:
    file_dict: dict[int, File]

    def __init__(self):
        self.file_dict = {}

    def creep(self, root: str):
        for root, _, files in os.walk(root, topdown=True):
            for file in files:
                abs = os.path.abspath(os.path.join(root, file))
                # ask for stat()
                stat = os.stat(abs)
                # eat a file to get hash
                md5 = hashlib_md5()
                with open(abs, 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data: break
                        md5.update(data)
                # create file entry
                file = File(file,
                            stat.st_size,
                            stat.st_mtime,
                            os.path.dirname(abs),
                            md5.hexdigest(),
                            Flags(stat.st_mode | 0b1000000000))
                self.file_dict[hash(file)] = file
