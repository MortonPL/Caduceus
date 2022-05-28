from fnmatch import filter as fnmatch_filter
from os.path import join as os_path_join
from src.file import File, Flags

BUF_SIZE = 65536

def analyze_flags_all(target: dict[int, File], dir: dict[int, File], desired_flags: Flags):
    for _, file in target.items():
        analyze_flags(file, desired_flags)

    for _, file in dir.items():
        analyze_flags(file, desired_flags)

def analyze_flags(file: File, desired_flags: Flags):
    if file.flags != desired_flags:
        file.state_flags[3] = True


def analyze_name_all(target: dict[int, File], dir: dict[int, File], illegal_chars: list[str]):
    for _, file in target.items():
        analyze_name(file, illegal_chars)

    for _, file in dir.items():
        analyze_name(file, illegal_chars)

def analyze_name(file: File, illegal_chars: list[str]):
         for char in illegal_chars:
            if char in file.name:
                file.state_flags[2] = True
                break   


def analyze_temp_all(target: dict[int, File], dir: dict[int, File], patterns: list[str]):
    for _, file in target.items():
        analyze_temp(file, patterns)

    for _, file in dir.items():
        analyze_temp(file, patterns)

def analyze_temp(file: File, patterns: list[str]):
    for string in patterns:
        if fnmatch_filter([file.name], string):
            file.state_flags[1] = True
            break


def analyze_duplicate_all(target: dict[int, File], dir: dict[int, File]):
    for thash, tfile in target.items():
        for _, dfile in dir.items():
            analyze_duplicate(tfile, dfile)
        for t2hash, t2file in target.items():
            if thash != t2hash:
                analyze_duplicate(tfile, t2file)

def analyze_duplicate(file1: File, file2: File):
    dupe = False
    if file1.hash == file2.hash:
        with open(os_path_join(file1.path, file1.name), 'rb') as tf:
            with open(os_path_join(file2.path, file2.name), 'rb') as df:
                while True:
                    ddata = df.read(BUF_SIZE)
                    tdata = tf.read(BUF_SIZE)
                    if ddata != tdata:
                        break
                    if not ddata and not tdata :
                        dupe = True
                        break
    if dupe:
        if file2.mtime > file1.mtime:
            file2.state_flags[4] = True
        else:
            file1.state_flags[4] = True


def analyze_samename_all(target: dict[int, File], dir: dict[int, File]):
    for thash, tfile in target.items():
        for _, dfile in dir.items():
            analyze_samename(tfile, dfile)
        for t2hash, t2file in target.items():
            if thash != t2hash:
                analyze_samename(tfile, t2file)

def analyze_samename(file1: File, file2: File):
    if file1.name == file2.name:
        if file2.mtime < file1.mtime:
            file2.state_flags[5] = True
        else:
            file1.state_flags[5] = True

def analyze_movable_all(target: dict[int, File], dir: dict[int, File]):
    for dhash, dfile in dir.items():
        for thash, tfile in target.items():
            if dfile.name == tfile.name:
                break
            dfile.state_flags[6] = True
