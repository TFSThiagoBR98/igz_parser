from dataclasses import dataclass
from struct import unpack

from lib.objects.objectNode import ObjectNode
from lib.utils import concat_hex_groups

@dataclass
class Vector3:
    name: str
    type: str
    offset: int
    lenght: int
    data: str
    floats: list

    @staticmethod
    def parser(node: ObjectNode, byd: str):
        data = concat_hex_groups(node.data)
        floats = unpack(f'{byd}LLLL4f', data)
        return Vector3(
            node.name,
            node.type,
            node.offset,
            node.lenght,
            node.data,
            floats
        )