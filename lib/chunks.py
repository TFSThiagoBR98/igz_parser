from dataclasses import dataclass, asdict
from io import BufferedReader
from typing import Literal

@dataclass
class ChunkInfo:
    offset: int
    size: int
    dataStartOffset: int
    pos: int
    data: str

def fetchChunks(igzFile: BufferedReader, byteorder: Literal["little", "big"] = "big"):
    chunks = []
    while True:
        pos = igzFile.tell()
        offset = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        size = int.from_bytes(igzFile.read(4), byteorder=byteorder)
        dataStartOffset = int.from_bytes(igzFile.read(8), byteorder=byteorder)

        if offset != 0:
            print(f"Sector found in Pos {offset} S: {size} and Data Start Offset: {dataStartOffset}")
            igzFile.seek(offset)
            data = igzFile.read(size).hex()
            igzFile.seek(pos + 16)
            chunks.append(ChunkInfo(offset, size, dataStartOffset, pos, data))
        else:
            # Move to the latest chunk descriptor
            igzFile.seek(pos)
            break
    return chunks