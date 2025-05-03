from dataclasses import dataclass, asdict
from io import BufferedReader
from typing import Literal

from lib.utils import decode_delta, decode_raw

@dataclass
class RHND:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    mapper: list

def processFixUpRHND(igzFile: BufferedReader, count: int, lenght: int, byteorder: Literal["little", "big"] = "big"):
    data = igzFile.read(lenght)
    return decode_delta(data, count, byteorder is "big")