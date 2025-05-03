from dataclasses import dataclass
from struct import unpack

from lib.objects.objectNode import ObjectNode

@dataclass
class CEntity:
    name: str
    type: str
    offset: int
    lenght: int
    data: str
    floats: list

    @staticmethod
    def parser(node: ObjectNode, byd: str):
        data = bytes.fromhex(node.data)
        floats = unpack(f'{byd}6f', data)
        return CEntity(
            node.name,
            node.type,
            node.offset,
            node.lenght,
            node.data,
            floats
        )