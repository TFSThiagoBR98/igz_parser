from dataclasses import dataclass

@dataclass
class FixUp:
    magicNumber: str
    offset: int
    count: int
    lenght: int
    startOfData: int
    data: str
