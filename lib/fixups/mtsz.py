from dataclasses import dataclass
from io import BufferedReader
from typing import Literal

@dataclass
class MTSZ:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    mapper: list

def processFixUpMTSZ(igzFile: BufferedReader, count: int, byteorder: Literal["little", "big"] = "big"):
    listInt = []
    x = 0
    while x < count:
        x += 1
        item = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        listInt.append(item)
    return listInt
