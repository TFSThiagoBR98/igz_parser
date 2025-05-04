from io import BufferedReader
from typing import Literal
from lib.chunks import ChunkInfo
from lib.fixups.onam import ONAM
from lib.fixups.tmet import TMET
from lib.fixups.tstr import TSTR
from lib.objects.classes.CEntity import CEntity
from lib.objects.classes.RangedFloat import RangedFloat
from lib.objects.classes.Vector3 import Vector3
from lib.objects.objectHeader import parserObjectHeader
from lib.objects.objectNode import ObjectList, ObjectListContent, ObjectNode
from lib.objects.offsetParser import parserObjectONAMOffset
from lib.utils import split_into_hex_groups

def parserObjectToClass(node: ObjectNode, byteorder: Literal["little", "big"] = "big"):
    byd: str
    if byteorder == "big":
        byd = ">"
    else:
        byd = "<"

    if node.type == "Vector3":
        return Vector3.parser(node, byd)
    elif node.type == "RangedFloat":
        return RangedFloat.parser(node, byd)
    elif node.type == "CEntity":
        return CEntity.parser(node, byd)
    else:
        return node
    
def processObjects(igzFile: BufferedReader, chunk: ChunkInfo, onam: ONAM, tstr: TSTR, tmet: TMET, byteorder: Literal["little", "big"] = "big"):
    print(f"Reading Data Chunk: {chunk.offset}")
    
    header = parserObjectHeader(igzFile, chunk.offset, byteorder)

    count = header.count
    spList = []
    offsetList = []
    orderedOffsetList = []

    print(f"Count: {count} {igzFile.tell()}")

    ## This list probably represents where in the content tree is the boxes
    print(f"Reading Offset Location List")
    x = 0
    while x < count:
        z = int.from_bytes(igzFile.read(8), byteorder=byteorder)
        print(f"Reading: {x} {z} in {igzFile.tell() - 8}")
        if z == 0:
            ## If Empty we ignore it
            print(f"WARNING: Found z = 0 when reading Offset location table: {igzFile.tell() - 8}")
            spList.append(z)
        else:
            offsetList.append(z)
            orderedOffsetList.append(z)
        x += 1
    print(f"Offset Location List complete: Where: {igzFile.tell()}, Size: {count * 8}")

    ## Fetch ONAM
    ## ONAM is the last block of data in the Object List
    onamV = chunk.offset + 40 + onam.offsetOnam
    igzFile.seek(onamV)
    print(f"Reading ONAM from: {igzFile.tell()}")
    strOffset = parserObjectONAMOffset(igzFile, onamV, count, byteorder)
    print(f"ONAM List complete: Where: {igzFile.tell()}, Size: {len(strOffset) * 16}")

    ## Now we read the Object Contents
    print(f"Reading Object Content List")
    v = 0
    objects = []

    ### Add the ONAM Offset list to the orderedOffsetList to allow the program to Read until it
    orderedOffsetList.append(onamV - chunk.offset)
    orderedOffsetList.sort()
    while v < len(offsetList):
        offset = offsetList[v]
        nextInOrder = chunk.offset + orderedOffsetList[orderedOffsetList.index(offset) + 1]

        # Go to the item
        pos = chunk.offset + offset
        igzFile.seek(pos)

        # Identify the Type and Name
        objType = int.from_bytes(igzFile.read(8), byteorder=byteorder) # Fetch Object Type
        typeId = tmet.strings[objType]
        typeName = tstr.strings[strOffset[v].strIndex]
        print(f"Reading: {v} {objType} in {igzFile.tell() - 8} {typeId}: {typeName}")

        objectSize = nextInOrder - offset - chunk.offset

        if objectSize < 0:
            raise Exception(f'Failed to parse Object Size, its negative {offsetList[v]} {nextInOrder}')

        # We cant determine the data Yet, because there is hidden Objects
        objectNode = ObjectNode(typeName, typeId, pos, objectSize, '', [], [], [])

        objects.append(objectNode)

        v += 1
        
    print(f"Object Content List complete")

    ## Now we read all objects to search for some offset

    print(f"Seaching Hidden Objects")
    obj: ObjectNode
    for obj in objects:
        igzFile.seek(obj.offset + 8) # We ignore the first byte
        size = 8
        while (size < obj.lenght):
            byt = int.from_bytes(igzFile.read(4), byteorder=byteorder)
            if byt in offsetList:
                print(f"Link detected in object {chunk.offset + byt}")
                obj.subnodesOffset.append(chunk.offset + byt)
            elif byt > 0 and byt < onamV and byt % 8 == 0:
                # print(f'Possible offset: {byt}')

                ## Now we check if this Offset is an Object
                curPos = igzFile.tell()
                igzFile.seek(chunk.offset + byt) # Go to this possible offset
                possibleType = int.from_bytes(igzFile.read(4), byteorder=byteorder) # Read the Data in it

                if 1 <= possibleType < len(tmet.strings):
                    print(f'Hidden Object Located: {tmet.strings[possibleType]} Offset: {chunk.offset + byt}')
                    obj.hiddenOffsets.append(chunk.offset + byt)
                    if byt not in orderedOffsetList:
                        orderedOffsetList.append(byt)
                # else:
                #     print(f'Not is an Object {possibleType} Offset: {byt}')

                igzFile.seek(curPos)

            size += 4

    print(f"Search Hidden Objects Complete")
    ## Now we need to recompute the data considering the hidden objects to then

    print(f"Computing Object Sizes")
    orderedOffsetList.sort()
    hiddenObjects = []
    v = 0
    while v < len(orderedOffsetList):
        offset = orderedOffsetList[v]
        nextIndex = orderedOffsetList.index(offset) + 1
        nextInOrder: int
        if (nextIndex < len(orderedOffsetList)):
            nextInOrder = chunk.offset + orderedOffsetList[nextIndex]
        elif offset == (onamV - chunk.offset):
            print(f"THE END")
            break
        else:
            nextInOrder = (onamV - chunk.offset)

        print(f"Computing Object {chunk.offset + offset} next is {nextInOrder}")

        if offset in offsetList:
            ## This offset is not Hidden, we can locate the Object and calculate his content
            obj = next(x for x in objects if x.offset == chunk.offset + offset)
            if obj == None:
                raise(Exception('Object not found'))
            idx = objects.index(obj)
            igzFile.seek(chunk.offset + offset)

            objectSize = nextInOrder - offset - chunk.offset

            if objectSize < 0:
                raise Exception(f'Failed to parse Object Size, its negative {offsetList[v]} {nextInOrder}')
            data = igzFile.read(objectSize)
            obj.data = split_into_hex_groups(data)
            obj.lenght = objectSize
            objects[idx] = obj
            pass
        else:
            print(f'Hidden Object {offset}')
            ## This is an Hidden Object, this not have an name but it have a type

            # Go to the item
            pos = chunk.offset + offset
            igzFile.seek(pos)

            # Identify the Type and Name
            objType = int.from_bytes(igzFile.read(4), byteorder=byteorder) # Fetch Object Type

            print(f"Object type is {objType}")
            typeId = tmet.strings[objType]

            objectSize = nextInOrder - offset - chunk.offset
            if objectSize < 0:
                raise Exception(f'Failed to parse Object Size, its negative {offsetList[v]} {nextInOrder}')
            data = igzFile.read(objectSize)

            objectNode = ObjectNode(v, typeId, pos, objectSize, split_into_hex_groups(data), [], [], [])
            hiddenObjects.append(objectNode)

            pass
        v += 1
        pass

    ## Now we pos process the objects to manipulate the data
    finalObjects = []
    obj: ObjectNode
    for obj in objects:
        finalObjects.append(parserObjectToClass(obj, byteorder))

    return ObjectList(
        chunk.offset,
        chunk.size,
        chunk.unknown,
        chunk.unknown2,
        chunk.pos,
        ObjectListContent(
            header,
            finalObjects,
            hiddenObjects
        )
    )