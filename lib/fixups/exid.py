from dataclasses import dataclass, asdict
from io import BufferedReader
from typing import Literal

@dataclass
class EXID:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    mapper: list

@dataclass
class EXIDMap:
    name: int
    type: int

def processFixUpEXID(igzFile: BufferedReader, count: int, byteorder: Literal["little", "big"] = "big"):
    mapper = []
    x = 0
    while x < count:
        x += 1
        name = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        type = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        mapper.append(EXIDMap(name, type))
    return mapper