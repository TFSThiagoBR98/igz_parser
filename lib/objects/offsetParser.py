from io import BufferedReader
from typing import Literal
from struct import unpack

from lib.fixups.onam import ONAMItem

def parserObjectOffset(igzFile: BufferedReader, offset: int, count: int, byteorder: Literal["little", "big"] = "big"):
    igzFile.seek(offset)
    size = count * 8

    byd: str
    if byteorder == "big":
        byd = ">"
    else:
        byd = "<"

    offsetListByt = igzFile.read(size)
    return unpack(f'{byd}{count}Q', offsetListByt)

def parserObjectONAMOffset(igzFile: BufferedReader, offset: int, count: int, byteorder: Literal["little", "big"] = "big"):
    igzFile.seek(offset)

    n = 0
    strOffsets = []
    while n < count:
        offset = int.from_bytes(igzFile.read(8), byteorder=byteorder)
        unknown = int.from_bytes(igzFile.read(8), byteorder=byteorder)
        strOffsets.append(ONAMItem(offset, unknown))
        n += 1

    return strOffsets