from dataclasses import dataclass, asdict
from io import BufferedReader
from typing import Literal
from struct import unpack

@dataclass
class Header:
    version: int
    crc: int
    unknown: int
    descriptorsCount: int

def parseHeader(igzFile: BufferedReader, byteorder: Literal["little", "big"] = "big"):
    igzFile.seek(4) ## Skip Magic Number
    header = igzFile.read(20)

    byd: str
    if byteorder == "big":
        byd = ">"
    else:
        byd = "<"

    version, crc, unknown, descriptorsCount = unpack(f'{byd}ILLQ', header)

    return Header(version, crc, unknown, descriptorsCount)