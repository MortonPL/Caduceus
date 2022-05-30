import stat
from os import chmod as os_chmod

from src.config import Config
from src.file import File, Flags
from src.prompt import prompt_flags

CODES = [stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
         stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
         stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]

def run_flag(target: dict[str, File], dir: dict[str, File], conf: Config) -> tuple[dict[str, File], dict[str, File]]:
    desired_flags = Flags(conf['default_file_permissions'])
    analyze_flags_all(target, dir, desired_flags)
    for fullname, file in target.items():
        if not file.state_flags[3]:
            continue
        if not prompt_flags(fullname, str(file.flags), str(desired_flags)):
            continue
        solve_flags(file, fullname, desired_flags)

    for fullname, file in dir.items():
        if not file.state_flags[3]:
            continue
        if not prompt_flags(fullname, str(file.flags), str(desired_flags)):
            continue
        solve_flags(file, fullname, desired_flags)

    return target, dir

def solve_flags(file: File, fullname: str, desired_flags: Flags) -> None:
    flags = 0

    for flag, code in zip(desired_flags, CODES):
        if flag is None:
            continue
        if flag:
            flags |= code
        else:
            flags &= ~code
    os_chmod(fullname, flags)
    file.state_flags[3] = False

def analyze_flags_all(target: dict[str, File], dir: dict[str, File], desired_flags: Flags):
    for _, file in target.items():
        analyze_flags(file, desired_flags)

    for _, file in dir.items():
        analyze_flags(file, desired_flags)

def analyze_flags(file: File, desired_flags: Flags):
    if file.flags != desired_flags:
        file.state_flags[3] = True
