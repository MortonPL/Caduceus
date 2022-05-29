from os import chmod as os_chmod
from os import remove as os_remove
from os.path import join as os_path_join
from copy import deepcopy
import stat
from src.file import File, Flags

CODES = [stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
         stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
         stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]

def solve_flags_all(target: dict[int, File], dir: dict[int, File], desired_flags: Flags) -> tuple[dict[int, File], dict[int, File]]:
    for _, file in target.items():
        if file.state_flags[3]:
            solve_flags(file, desired_flags)

    for _, file in dir.items():
        if file.state_flags[3]:
            solve_flags(file, desired_flags)

    return target, dir

def solve_flags(file: File, desired_flags: Flags):
    flags = 0

    for flag, code in zip(desired_flags, CODES):
        if flag is None:
            continue
        if flag:
            flags |= code
        else:
            flags &= ~code
    os_chmod(os_path_join(file.path, file.name), flags)
    file.state_flags[3] = False

def solve_dupes_all(target: dict[int, File], dir: dict[int, File]) -> tuple[dict[int, File], dict[int, File]]:
    new_target = deepcopy(target)
    for hash, file in target.items():
        if file.state_flags[4]:
            solve_dupes(file)
            new_target.pop(hash)
    target = new_target

    new_dir = deepcopy(dir)
    for hash, file in dir.items():
        if file.state_flags[4]:
            solve_dupes(file)
            new_dir.pop(hash)
    dir = new_dir

    return new_target, new_dir

def solve_dupes(file: File):
    os_remove(os_path_join(file.path, file.name))

def solve_empty_all(target: dict[int, File], dir: dict[int, File]) -> tuple[dict[int, File], dict[int, File]]:
    new_target = deepcopy(target)
    for hash, file in target.items():
        if file.state_flags[0]:
            solve_empty(file)
            new_target.pop(hash)
    target = new_target

    new_dir = deepcopy(dir)
    for hash, file in dir.items():
        if file.state_flags[0]:
            solve_empty(file)
            new_dir.pop(hash)
    dir = new_dir

    return new_target, new_dir

def solve_empty(file: File):
    os_remove(os_path_join(file.path, file.name))

def solve_temp_all(target: dict[int, File], dir: dict[int, File]) -> tuple[dict[int, File], dict[int, File]]:
    new_target = deepcopy(target)
    for hash, file in target.items():
        if file.state_flags[1]:
            solve_temp(file)
            new_target.pop(hash)
    target = new_target

    new_dir = deepcopy(dir)
    for hash, file in dir.items():
        if file.state_flags[1]:
            solve_temp(file)
            new_dir.pop(hash)
    dir = new_dir

    return new_target, new_dir

def solve_temp(file: File):
    os_remove(os_path_join(file.path, file.name))
