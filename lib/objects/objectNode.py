from dataclasses import dataclass

from lib.objects.objectHeader import ObjectListHeader

@dataclass
class ObjectNode:
    name: str
    type: str
    offset: int
    lenght: int
    data: list
    subnodesOffset: list
    hiddenOffsets: list
    hiddenObjects: list

@dataclass
class ObjectListContent:
    header: ObjectListHeader
    objects: list
    hiddenObjects: list

@dataclass
class ObjectList:
    offset: int
    size: int
    dataStartOffset: int
    pos: int
    content: ObjectListContent
