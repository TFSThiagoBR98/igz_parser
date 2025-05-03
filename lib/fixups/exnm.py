from dataclasses import dataclass
from io import BufferedReader
from typing import Literal

@dataclass
class EXNM:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    mapper: list

@dataclass
class EXNMMap:
    name: str
    nameA: int
    type: str
    typeA: int

def processFixUpEXNM(igzFile: BufferedReader, count: int, strings: list, byteorder: Literal["little", "big"] = "big"):
    mapper = []
    x = 0
    while x < count:
        x += 1
        name = int.from_bytes(igzFile.read(2), byteorder=byteorder)
        nameA = int.from_bytes(igzFile.read(2), byteorder=byteorder)
        type = int.from_bytes(igzFile.read(2), byteorder=byteorder)
        typeA = int.from_bytes(igzFile.read(2), byteorder=byteorder)
        mapper.append(EXNMMap(strings[name], nameA, strings[type], typeA))
    return mapper
