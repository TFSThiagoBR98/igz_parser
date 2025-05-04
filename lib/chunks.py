from dataclasses import dataclass, asdict
from io import BufferedReader
from typing import Literal

@dataclass
class ChunkInfo:
    offset: int
    size: int
    unknown: int
    unknown2: int
    pos: int
    data: str

def fetchChunks(igzFile: BufferedReader, byteorder: Literal["little", "big"] = "big"):
    chunks = []
    while True:
        pos = igzFile.tell()
        offset = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        size = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        unknown1 = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        unknown2 = int.from_bytes(igzFile.read(4), byteorder=byteorder)

        if offset != 0:
            print(f"Sector found in Pos {offset} S: {size} and {unknown1}/{unknown2}")
            igzFile.seek(offset)
            data = igzFile.read(size).hex()
            igzFile.seek(pos + 16)
            chunks.append(ChunkInfo(offset, size, unknown1, unknown2, pos, data))
        else:
            # Move to the latest chunk descriptor
            igzFile.seek(pos)
            break
    return chunks