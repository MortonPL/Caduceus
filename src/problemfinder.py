from src.file import File, Flags

def analyze_flags_all(target: dict[str, File], dir: dict[str, File], desired_flags: Flags):
    for _, file in target.items():
        analyze_flags(file, desired_flags)

    for _, file in dir.items():
        analyze_flags(file, desired_flags)

def analyze_flags(file: File, desired_flags: Flags):
    if file.flags != desired_flags:
        file.state_flags[3] = True


def analyze_name_all(target: dict[str, File], dir: dict[str, File], illegal_chars: list[str]):
    for _, file in target.items():
        analyze_name(file, illegal_chars)

    for _, file in dir.items():
        analyze_name(file, illegal_chars)

def analyze_name(file: File, illegal_chars: list[str]):
         for char in illegal_chars:
            if char in file.name:
                file.state_flags[2] = True
                break


def analyze_samename_all(target: dict[str, File], dir: dict[str, File]):
    for fullpath1, tfile in target.items():
        for _, dfile in dir.items():
            analyze_samename(tfile, dfile)
        for fullpath2, t2file in target.items():
            if fullpath1 != fullpath2:
                analyze_samename(tfile, t2file)

def analyze_samename(file1: File, file2: File):
    if file1.name == file2.name:
        if file2.mtime <= file1.mtime:
            file2.state_flags[5] = True
        else:
            file1.state_flags[5] = True

def analyze_movable_all(target: dict[str, File], dir: dict[str, File]):
    for _, dfile in dir.items():
        for _, tfile in target.items():
            if dfile.name == tfile.name:
                break
            dfile.state_flags[6] = True
