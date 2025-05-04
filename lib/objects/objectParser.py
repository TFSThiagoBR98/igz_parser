from typing import Literal
from lib.objects.classes.CEntity import CEntity
from lib.objects.classes.RangedFloat import RangedFloat
from lib.objects.classes.Vector3 import Vector3
from lib.objects.objectNode import ObjectNode

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