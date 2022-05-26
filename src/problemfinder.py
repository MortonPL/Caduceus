import fnmatch
from src.file import File, Flags

def analyze_flags(target: dict[int, File], dir: dict[int, File], desired_flags: Flags):
    for _, file in target.items():
        if file.flags != desired_flags:
            file.state_flags[3] = True

    for _, file in dir.items():
        if file.flags != desired_flags:
            file.state_flags[3] = True

def analyze_names(target: dict[int, File], dir: dict[int, File], illegal_chars: list[str]):
    for _, file in target.items():
        for char in illegal_chars:
            if char in file.name:
                file.state_flags[2] = True
                break

    for _, file in dir.items():
        for char in illegal_chars:
            if char in file.name:
                file.state_flags[2] = True
                break

def analyze_temp(target: dict[int, File], dir: dict[int, File], patterns: list[str]):
    for _, file in target.items():
        for string in patterns:
            if fnmatch.filter((file.name), string):
                file.state_flags[1] = True
                break

    for _, file in dir.items():
        for string in patterns:
            if fnmatch.filter([file.name], string):
                file.state_flags[1] = True
                break

def analyze_duplicates(target: dict[int, File], dir: dict[int, File]):
    pass

def analyze_movables(target: dict[int, File], dir: dict[int, File]):
    pass
