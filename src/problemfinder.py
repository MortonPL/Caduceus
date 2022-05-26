from src.file import File, Flags

def analyze_flags(target: dict[int, File], dir: dict[int, File], desired_flags: Flags):
    for _, file in target.items():
        if file.flags != desired_flags:
            file.state_flags[3] = True

    for _, file in dir.items():
        if file.flags != desired_flags:
            file.state_flags[3] = True
