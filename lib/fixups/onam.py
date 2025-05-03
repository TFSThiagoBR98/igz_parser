from dataclasses import dataclass
from io import BufferedReader
from typing import Literal

@dataclass
class ONAM:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    offsetOnam: int

@dataclass
class ONAMItem:
    strIndex: int
    b: int

def processFixUpONAM(igzFile: BufferedReader, count: int, byteorder: Literal["little", "big"] = "big"):
    return int.from_bytes(igzFile.read(4), byteorder=byteorder)
