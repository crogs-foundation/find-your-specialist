from typing import TypedDict


class Specialist(TypedDict):
    label: str
    prompt: str
    opened: bool


Context = dict[str, Specialist]
