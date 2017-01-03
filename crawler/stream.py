from typing import Any, List, Set, TypeVar, Generic, Iterator, Callable, Sequence

"""This file contains a slightly modified version of
praw/models/util.py"""

T = TypeVar('T', bound=Any)

class BoundedSet(Generic[T]):
    def __init__(self, max_items: int) -> None:
        self.max_items = max_items  # type: int
        self._fifo = []  # type: List[T]
        self._set = set()  # type: Set[T]

    def __contains__(self, item: T) -> bool:
        return item in self._set

    def add(self, item: T) -> None:
        if len(self._set) == self.max_items:
            self._set.remove(self._fifo.pop(0))
        self._fifo.append(item)
        self._set.add(item)


def stream_items(function: Callable[..., Sequence[T]]) -> Iterator[List[T]]:
    before_fullname = None
    seen_fullnames = BoundedSet(301)  # type: BoundedSet[T]
    without_before_counter = 0
    while True:
        newest_fullname = None
        limit = 100
        if before_fullname is None:
            limit -= without_before_counter
            without_before_counter = (without_before_counter + 1) % 30
        out = []
        for item in reversed(list(function(
                limit=limit, params={'before': before_fullname}))):
            if item.fullname in seen_fullnames:
                continue
            seen_fullnames.add(item.fullname)
            newest_fullname = item.fullname
            out.append(item)
        yield out 
        before_fullname = newest_fullname
