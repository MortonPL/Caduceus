class GenericFlags(list):
    pattern: str

    def __init__(self, *args) -> None:
        super(GenericFlags, self).__init__()
        if len(args) < 2:
            return
        if isinstance(args[1], str):
            self.pattern = args[1]
        if len(args) < 3:
            caller = GenericFlags
        else:
            caller = args[2]

        if isinstance(args[0], int):
            self.extend([(args[0] & 2**mask) == 2**mask for mask in range(len(self.pattern) - 1, -1, -1)])
        elif isinstance(args[0], str):
            self.extend(caller.revstr(self, args[0]))
        elif isinstance(args[0], list):
            self.extend(args[0])


    def revstr(self, chars) -> list:
        return [inchar == patchar for inchar, patchar in zip(chars, self.pattern)]


    def __str__(self) -> str:
        return "".join([char if bit else '-' for bit, char in zip(self, self.pattern)])


    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, GenericFlags):
            return False
        for x, y in zip(self, __o):
            if x != y:
                return False
        return True
    

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)


class Flags(GenericFlags):
    pattern = 'rwxrwxrwx'


    def __init__(self, args) -> None:
        super(Flags, self).__init__(args, self.pattern, Flags)


    def revstr(self, chars: str) -> list:
        flags = [False] * len(self.pattern)
        for i in range(len(self.pattern)):
            if chars[i] == self.pattern[i]:
                flags[i] = True
            elif chars[i] == '_':
                flags[i] = None # type: ignore
        return flags


    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Flags):
            return False
        for x, y in zip(self, __o):
            if x != None and y != None and x != y:
                return False
        return True


class File:
    name: str
    size: int
    mtime: float
    path: str
    hash: str
    flags: Flags
    state_flags: GenericFlags
    ref_file: str


    def __init__(self, name: str, size: int, mtime: float, path: str, hash: str, flags: Flags) -> None:
        self.name = name
        self.size = size
        self.mtime = mtime
        self.path = path
        self.hash = hash
        self.flags = flags

                                        #empty           temp   name   flags  dupe   samename movable
        self.state_flags = GenericFlags([self.size == 0, False, False, False, False, False,   False], "etnfdsm")
        self.ref_file = ''


    def __repr__(self) -> str:
        data = ", ".join([self.name, str(self.size), str(self.mtime), self.path, self.hash, str(self.flags), str(self.state_flags)])
        return f"File({data})"
