from abc import ABC, abstractmethod
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..utils.result import Result


class Technique(ABC):
    """Protocol class for defining callable techniques.

    Attributes:
        __init__(): Class initializer.
        __call__(): @abstractmethod to allow callable functionality.
        __iter__(): Allows :func:`__call__()` to act as a generator.
        __next__(): Standard iterator implementation.
    """

    def __init__(self, sequence) -> None:
        self._sequence = sequence
        self._index = 0

    @abstractmethod
    def __call__(self) -> Generator[Result]: ...

    def __iter__(self) -> Generator[Callable[..., Result]]:
        yield from self.__call__()

    def __next__(self) -> object:
        if self._index < len(self._sequence):
            item = self._sequence[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration
