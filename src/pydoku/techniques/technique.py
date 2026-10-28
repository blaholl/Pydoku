from typing import Protocol


class Technique(Protocol):
    """Protocol class for defining callable techniques.

    Attributes:
        __init__(): Class initializer
        __call__(): Callable functionality
        __iter__(): Allows :func:`__call__()` to act as a generator.
    """

    def __init__(self): ...

    def __call__(self): ...

    def __iter__(self): ...
