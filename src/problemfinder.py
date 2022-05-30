from src.file import File, Flags

def analyze_movable_all(target: dict[str, File], dir: dict[str, File]):
    for _, dfile in dir.items():
        for _, tfile in target.items():
            if dfile.name == tfile.name:
                break
            dfile.state_flags[6] = True
