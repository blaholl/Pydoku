from typing import Protocol


class Technique(Protocol):
    def check(self): ...
