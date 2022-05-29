from os.path import join as os_path_join

from src.file import File

OPTIONS = "([Y]es/[a]ll/[n]o/[s]kip)"
CACHE = [0]*7

def prompt(string: str, cache_index: int) -> bool:
    if CACHE[cache_index] == 1:
        return False
    elif CACHE[cache_index] == 2:
        return True
    while True:
        re = input(string)
        if len(re) == 0:
            return True
        re = re.lower()[0]
        if re == 'y':
            return True
        elif re == 'n':
            return False
        elif re == 'a':
            CACHE[cache_index] = 2
            return True
        elif re == 's':
            CACHE[cache_index] = 1
            return False
        else:
            continue


def prompt_empty(filename: str) -> bool:
    strings = [filename, "is empty. Remove?", OPTIONS, ""]
    return prompt(" ".join(strings), 0)


def prompt_temp(filename: str) -> bool:
    strings = [filename, "is a temporary file. Remove?", OPTIONS, ""]
    return prompt(" ".join(strings), 1)

def prompt_dupes(filename1: str, filename2: str) -> bool:
    strings = [filename1, "has the same contents as",
               filename2, ", remove former?", OPTIONS, ""]
    return prompt(" ".join(strings), 2)
