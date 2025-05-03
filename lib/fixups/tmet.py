from dataclasses import dataclass
from io import BufferedReader
from typing import Literal

from lib.utils import readString

@dataclass
class TMET:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    strings: list

def processFixUpTMET(igzFile: BufferedReader, count: int, byteorder: Literal["little", "big"] = "big"):
    strings = []
    x = 0
    while x < count:
        x += 1
        strings.append(readString(igzFile))
    return strings
