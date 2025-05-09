from dataclasses import dataclass
from struct import unpack

from lib.objects.objectNode import ObjectNode
from lib.utils import concat_hex_groups

@dataclass
class CEntity:
    name: str
    type: str
    offset: int
    lenght: int
    data: str
    x: float
    y: float
    z: float

    @staticmethod
    def parser(node: ObjectNode, byd: str):
        data = node.data
        classData = data[4:]
        coodr = concat_hex_groups(classData[4:7])
        x, y, z = unpack(f'{byd}3f', coodr)
        
        return CEntity(
            node.name,
            node.type,
            node.offset,
            node.lenght,
            node.data,
            x,
            y,
            z
        )