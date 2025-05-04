from dataclasses import dataclass, asdict
from io import BufferedReader
from typing import Literal
from struct import unpack

@dataclass
class ObjectListHeader:
    padding: str
    count: int
    unknown: str

def parserObjectHeader(igzFile: BufferedReader, offset: int, sectorStart: int, byteorder: Literal["little", "big"] = "big"):
    igzFile.seek(offset)

    padding = igzFile.read(sectorStart)
    headerByt = igzFile.read(24)

    byd: str
    if byteorder == "big":
        byd = ">"
    else:
        byd = "<"

    count, unknown = unpack(f'{byd}I20s', headerByt)

    return ObjectListHeader(padding.hex(), count, unknown.hex())