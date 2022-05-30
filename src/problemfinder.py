from src.file import File, Flags

def analyze_flags_all(target: dict[str, File], dir: dict[str, File], desired_flags: Flags):
    for _, file in target.items():
        analyze_flags(file, desired_flags)

    for _, file in dir.items():
        analyze_flags(file, desired_flags)

def analyze_flags(file: File, desired_flags: Flags):
    if file.flags != desired_flags:
        file.state_flags[3] = True


def analyze_movable_all(target: dict[str, File], dir: dict[str, File]):
    for _, dfile in dir.items():
        for _, tfile in target.items():
            if dfile.name == tfile.name:
                break
            dfile.state_flags[6] = True
