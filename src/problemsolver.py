from os import chmod as os_chmod
from os.path import join as os_path_join
import stat
from src.file import File, Flags

CODES = [stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
         stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
         stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]

def solve_flags_all(target: dict[int, File], dir: dict[int, File], desired_flags: Flags):
    for _, file in target.items():
        if file.state_flags[3]:
            solve_flags(file, desired_flags)

    for _, file in dir.items():
        if file.state_flags[3]:
            solve_flags(file, desired_flags)

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
