import os
import hashlib
from src.file import File, bits2attribs

SIZE = 65536

class Creeper:
    file_list: list[File]

    def __init__(self):
        self.file_list = []

    def walk(self, root):
        for root, dirs, files in os.walk(root, topdown=True):
            for file in files:
                abs = os.path.abspath(os.path.join(root, file))
                # ask for stat()
                stat = os.stat(abs)
                # eat a file to get hash
                md5 = hashlib.md5()
                with open(abs, 'rb') as f:
                    while True:
                        data = f.read(SIZE)
                        if not data: break
                        md5.update(data)
                # create file entry
                self.file_list.append(File(file,
                                           stat.st_size,
                                           stat.st_mtime,
                                           os.path.dirname(abs),
                                           md5.hexdigest(),
                                           bits2attribs(stat.st_mode)))
