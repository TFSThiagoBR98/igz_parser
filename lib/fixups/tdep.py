from dataclasses import dataclass
from io import BufferedReader
from typing import Literal

from lib.utils import readString

@dataclass
class TDEP:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    dependencies: list

def processFixUpTDEP(igzFile: BufferedReader, count: int, byteorder: Literal["little", "big"] = "big"):
    dependencies = []
    x = 0
    while x < count:
        x += 1
        dependencies.append(readString(igzFile))
    return dependencies
