# src/models/selection.py
from dataclasses import dataclass, field
from typing import List

from src.core.base_types import GameConfig
from src.core.combination_generator import CombinationGenerator
from src.core.game_validator import GameValidator
from .ticket import Ticket


@dataclass
class Selection:
    """Representa uma seleção de números para gerar combinações."""
    numbers: List[int] = field(default_factory=list)
    config: GameConfig = field(default_factory=GameConfig)
    validator: GameValidator = field(init=False)
    generator: CombinationGenerator = field(init=False)

    def __post_init__(self):
        self.validator = GameValidator(self.config)
        self.generator = CombinationGenerator(self.config)

    def add_number(self, number: int) -> bool:
        """Adiciona um número à seleção."""
        if len(self.numbers) >= self.config.NUMBERS_TO_SELECT:
            return False

        if number in self.numbers:
            return False

        if not self.config.MIN_NUMBER <= number <= self.config.MAX_NUMBER:
            return False

        self.numbers.append(number)
        return True

    def remove_number(self, number: int) -> bool:
        """Remove um número da seleção."""
        if number in self.numbers:
            self.numbers.remove(number)
            return True
        return False

    def clear(self) -> None:
        """Limpa a seleção."""
        self.numbers.clear()

    def is_complete(self) -> bool:
        """Verifica se a seleção está completa."""
        return len(self.numbers) == self.config.NUMBERS_TO_SELECT

    def generate_tickets(self) -> List[Ticket]:
        """Gera ‘tickets’ a partir da seleção atual."""
        if not self.is_complete():
            raise ValueError("Seleção incompleta para gerar tickets")

        combinations = self.generator.process_numbers(self.numbers)
        return [Ticket(numbers=combination) for combination in combinations]

    def set_numbers(self, sequence):
        """Define os números da seleção."""
        self.numbers = sequence


