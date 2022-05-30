OPTIONS = "([Y]es/[a]ll/[n]o/[s]kip)"
CACHE = [0]*7

def prompt(string: str, cache_index: int) -> bool:
    # if already responded with all or skip, don't ask
    if CACHE[cache_index] == 1:
        return False
    elif CACHE[cache_index] == 2:
        return True
    # expect only these responses
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
    strings = [filename, " is empty. Remove? ", OPTIONS, " "]
    return prompt("".join(strings), 0)

def prompt_temp(filename: str) -> bool:
    strings = [filename, " is a temporary file. Remove? ", OPTIONS, " "]
    return prompt("".join(strings), 1)

def prompt_dupe(filename1: str, filename2: str) -> bool:
    strings = [filename1, " has the same contents as ",
               filename2, ", remove former? ", OPTIONS, " "]
    return prompt("".join(strings), 2)

def prompt_name(filename1: str) -> bool:
    strings = [filename1, "'s name contains illegal characters, replace? ",
               OPTIONS, " "]
    return prompt("".join(strings), 3)

def prompt_samename(filename1: str, filename2: str) -> bool:
    strings = [filename1, " has the same name as ",
               filename2, ", remove former? ", OPTIONS, " "]
    return prompt("".join(strings), 4)

def prompt_move(filename1: str, filename2: str) -> bool:
    strings = [filename1, " is a file not yet in target dir. Expected directory: ",
               filename2, ", move? ", OPTIONS, " "]
    return prompt("".join(strings), 5)

def prompt_flags(filename: str, badflags: str, goodflags: str) -> bool:
    strings = [filename, " has different permissions ",
               badflags, " from default ", goodflags, ", apply default? ", OPTIONS, " "]
    return prompt("".join(strings), 6)
