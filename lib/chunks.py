from dataclasses import dataclass, asdict

@dataclass
class ChunkInfo:
    offset: int
    size: int
    unknown: int
    unknown2: int
    pos: int
    data: str

def parserChunks():
    pass