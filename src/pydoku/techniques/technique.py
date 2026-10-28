from collections.abc import Callable, Generator
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ..utils.result import Result


class Technique(Protocol):
    """Protocol class for defining callable techniques.

    Attributes:
        __init__(): Class initializer
        __call__(): Callable functionality
        __iter__(): Allows :func:`__call__()` to act as a generator.
    """

    def __init__(self): ...

    def __call__(self) -> Generator[Result]: ...

    def __iter__(self) -> Generator[Callable[..., Result]]:
        yield from self.__call__()
