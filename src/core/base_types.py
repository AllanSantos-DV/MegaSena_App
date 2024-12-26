# src/core/base_types.py
from dataclasses import dataclass
from typing import List

Numbers = List[int]
Groups = List[List[int]]


@dataclass
class GameConfig:
    MIN_NUMBER: int = 1
    MAX_NUMBER: int = 60
    NUMBERS_PER_GAME: int = 6
    NUMBERS_TO_SELECT: int = 12

    @property
    def valid_range(self) -> range:
        return range(self.MIN_NUMBER, self.MAX_NUMBER + 1)
