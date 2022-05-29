from copy import deepcopy
from os import remove as os_remove
from os.path import join as os_path_join

from src.file import File
from src.prompt import prompt_dupes

BUF_SIZE = 65536

def run_dupes(target: dict[str, File], dir: dict[str, File]) -> tuple[dict[str, File], dict[str, File]]:
    analyze_duplicate_all(target, dir)

    new_target = deepcopy(target)
    for fullname, file in target.items():
        if not file.state_flags[4]:
            continue
        if not prompt_dupes(fullname, file.ref_file):
            continue
        solve_dupes(target, dir, file, fullname)
        new_target.pop(fullname)
    target = new_target

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if not file.state_flags[4]:
            continue
        if not prompt_dupes(fullname, file.ref_file):
            continue
        solve_dupes(target, dir, file, fullname)
        new_dir.pop(fullname)
    dir = new_dir

    return new_target, new_dir


def solve_dupes(target: dict[str, File], dir: dict[str, File], file: File, file_fullname: str) -> None:
    os_remove(file_fullname)
    for tfile in target.values():
        if tfile.ref_file == file_fullname:
            tfile.ref_file = file.ref_file
    for dfile in dir.values():
        if dfile.ref_file == file_fullname:
            dfile.ref_file = file.ref_file


def analyze_duplicate_all(target: dict[str, File], dir: dict[str, File]):
    for tfullname, tfile in target.items():
        for dfullname, dfile in dir.items():
            analyze_duplicate(tfile, dfile, tfullname, dfullname)
        for t2fullname, t2file in target.items():
            if tfullname != t2fullname:
                analyze_duplicate(tfile, t2file, tfullname, t2fullname)


def analyze_duplicate(file1: File, file2: File, file1_fullname: str, file2_fullname: str):
    dupe = False
    if file1.hash == file2.hash:
        with open(file1_fullname, 'rb') as tf:
            with open(file2_fullname, 'rb') as df:
                while True:
                    ddata = df.read(BUF_SIZE)
                    tdata = tf.read(BUF_SIZE)
                    if ddata != tdata:
                        break
                    if not ddata and not tdata :
                        dupe = True
                        break
    if dupe:
        if file2.mtime >= file1.mtime:
            file2.state_flags[4] = True
            file2.ref_file = file1_fullname
        else:
            file1.state_flags[4] = True
            file1.ref_file = file2_fullname
