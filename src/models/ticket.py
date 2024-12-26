# src/models/ticket.py
from dataclasses import dataclass

from src.core.base_types import Numbers
from src.core.game_validator import GameValidator


@dataclass
class Ticket:
    numbers: Numbers
    validator: GameValidator = GameValidator()

    def __post_init__(self):
        """Valida os números ao criar o ticket."""
        if not self.validator.validate_game(self.numbers):
            raise ValueError("Números inválidos para um ticket válido")
        self.numbers = sorted(self.numbers)

    def __len__(self) -> int:
        return len(self.numbers)

    def __contains__(self, number: int) -> bool:
        return number in self.numbers

    def __eq__(self, other: 'Ticket') -> bool:
        if not isinstance(other, Ticket):
            return False
        return self.numbers == other.numbers

    def __str__(self) -> str:
        return f"Ticket({', '.join(map(str, self.numbers))})"

    def matches_with(self, result: Numbers) -> int:
        """Retorna quantidade de números que acertou com o resultado."""
        return len(set(self.numbers).intersection(set(result)))
