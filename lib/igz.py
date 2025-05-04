from base64 import b64encode
from dataclasses import dataclass
from io import BufferedReader
from typing import Literal

from lib.chunks import ChunkInfo, fetchChunks
from lib.fixup import processFixUp
from lib.header import Header, parseHeader
from lib.objects.objectNode import ObjectList
from lib.objects.objectParser import processObjects

@dataclass
class IgzFile:
    header: Header
    filler: str
    descriptors: list
    objList: ObjectList

def processIgz(igzFile: BufferedReader, byteorder: Literal["little", "big"] = "big"):
    # FORMAT: VERSION + CRC + UNKNOWN + FIXUP COUNT + CHUNK DESCRIPTOR + EMPTY DATA
    header = parseHeader(igzFile, byteorder)
    
    print(f"Version: {header.version}")
    print(f"CRC: {header.crc}")
    print(f"Unknown1: {header.unknown}")
    print(f"Fixup Count: {header.descriptorsCount}")
    
    chunks = fetchChunks(igzFile, byteorder)
    
    # The first chunk is an Descriptor for the contents in the second chunk (object list)
    fixups: ChunkInfo = chunks[0]

    #Save content from current until first chunk content
    currentPos = igzFile.tell()
    fixupStartPos = fixups.offset
    fillerContent = b64encode(igzFile.read(fixupStartPos - currentPos)).decode()

    print(f'Processing fixups in {fixups.offset}')
    fixupList = processFixUp(igzFile, fixups, byteorder)

    objectList: ChunkInfo = chunks[1]
    objectListProcessed = processObjects(igzFile, objectList, fixupList['ONAM'], fixupList['TSTR'], fixupList['TMET'], byteorder)

    igzFile = IgzFile(header, fillerContent, fixupList, objectListProcessed)

    return igzFile