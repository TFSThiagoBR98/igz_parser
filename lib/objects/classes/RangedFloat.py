from dataclasses import dataclass
from struct import unpack

from lib.objects.objectNode import ObjectNode
from lib.utils import concat_hex_groups

@dataclass
class RangedFloat:
    name: str
    type: str
    offset: int
    lenght: int
    data: str
    floats: list

    @staticmethod
    def parser(node: ObjectNode, byd: str):
        data = concat_hex_groups(node.data)

        ## In this format 16 bytes are the Header?
        floatSize = int((node.lenght - 16) / 4)

        floats = unpack(f'{byd}LLLL{floatSize}f', data)
        return RangedFloat(
            node.name,
            node.type,
            node.offset,
            node.lenght,
            node.data,
            floats
        )