"""Types and Custom Types"""

from dataclasses import dataclass
from typing import Any, Iterable, Dict, List

DictStrAny = Dict[str, Any]
IterableStr = Iterable[str]
ListStr = List[str]

EnvironPath = str | IterableStr


@dataclass
class KeyParsed:
    """Data type Identifier Parsed
    """

    identifier: str
    parser: Any
    args: ListStr


__all__ = [
    'Any',
    'Dict',
    'DictStrAny',
    'EnvironPath',
    'Iterable',
    'IterableStr',
    'KeyParsed',
    'List',
    'ListStr',
]
