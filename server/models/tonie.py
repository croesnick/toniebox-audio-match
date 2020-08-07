from dataclasses import dataclass


@dataclass(frozen=True)
class Household:
    id: str


@dataclass(frozen=True)
class Tonie:
    id: str
    household: Household
    name: str
    image: str
