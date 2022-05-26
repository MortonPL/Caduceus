from datetime import date

def bits2attribs(bits: int) -> tuple:
    return (
        bits & 0b1000000000 == 512,
        bits & 0b0100000000 == 256,
        bits & 0b0010000000 == 128,
        bits & 0b0001000000 == 64,
        bits & 0b0000100000 == 32,
        bits & 0b0000010000 == 16,
        bits & 0b0000001000 == 8,
        bits & 0b0000000100 == 4,
        bits & 0b0000000010 == 2,
        bits & 0b0000000001 == 1
    )

def attribs2str(attribs: tuple) -> str:
    return "".join([
        'd' if attribs[0] else '-',
        'r' if attribs[1] else '-',
        'w' if attribs[2] else '-',
        'x' if attribs[3] else '-',
        'r' if attribs[4] else '-',
        'w' if attribs[5] else '-',
        'x' if attribs[6] else '-',
        'r' if attribs[7] else '-',
        'w' if attribs[8] else '-',
        'x' if attribs[9] else '-',
    ])

class File:
    name: str
    size: int
    mtime: float
    path: str
    hash: str
    attribs: tuple

    is_empty: bool
    is_temp: bool
    is_funny: bool
    is_funny_attribs: bool

    def __init__(self, name, size, mtime, path, hash, attribs) -> None:
        self.name = name
        self.size = size
        self.mtime = mtime
        self.path = path
        self.hash = hash
        self.attribs = attribs

        self.is_empty = size == 0
        self.is_temp = False
        self.is_funny = False
        self.is_funny_attribs = False

    def __repr__(self) -> str:
        data = ", ".join([self.name, str(self.size), str(self.mtime), self.path, self.hash, attribs2str(self.attribs)])
        return f"File({data})"
