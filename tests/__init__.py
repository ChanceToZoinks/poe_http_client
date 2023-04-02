from typing import Any, Callable, Generic, Iterable, TypeVar

from pytest import mark


def has_all_keys(o: Any, keys: list[str]) -> bool:
    for k in keys:
        if not k in o:
            return False
    return True
