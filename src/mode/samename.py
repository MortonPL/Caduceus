from copy import deepcopy
from os import remove as os_remove

from src.config import Config
from src.file import File
from src.prompt import prompt_samename

def run_samename(target: dict[str, File], dir: dict[str, File], conf: Config) -> tuple[dict[str, File], dict[str, File]]:
    analyze_samename_all(target, dir)
    new_target = deepcopy(target)
    for fullname, file in target.items():
        if not file.state_flags[5]:
            continue
        if not prompt_samename(fullname, file.ref_file):
            continue
        solve_samename(target, dir, file, fullname)
        new_target.pop(fullname)
    target = new_target

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if not file.state_flags[5]:
            continue
        if not prompt_samename(fullname, file.ref_file):
            continue
        solve_samename(target, dir, file, fullname)
        new_dir.pop(fullname)
    dir = new_dir

    return new_target, new_dir

def solve_samename(target: dict[str, File], dir: dict[str, File], file: File, file_fullname: str) -> None:
    os_remove(file_fullname)
    for tfile in target.values():
        if tfile.ref_file == file_fullname:
            tfile.ref_file = file.ref_file
    for dfile in dir.values():
        if dfile.ref_file == file_fullname:
            dfile.ref_file = file.ref_file

def analyze_samename_all(target: dict[str, File], dir: dict[str, File]):
    for fullpath1, tfile in target.items():
        for dfullname, dfile in dir.items():
            analyze_samename(tfile, dfile, fullpath1, dfullname)
        for fullpath2, t2file in target.items():
            if fullpath1 != fullpath2:
                analyze_samename(tfile, t2file, fullpath1, fullpath2)

def analyze_samename(file1: File, file2: File, file1_fullname: str, file2_fullname: str):
    if file1.name == file2.name:
        if file2.mtime <= file1.mtime:
            file2.state_flags[5] = True
            file2.ref_file = file1_fullname
        else:
            file1.state_flags[5] = True
            file1.ref_file = file2_fullname
