# src/core/game_validator.py
from .base_types import GameConfig, Numbers


class GameValidator:
    def __init__(self, config: GameConfig = GameConfig()):
        self.config = config

    def validate_numbers(self, numbers: Numbers) -> bool:
        """Valida se os números estão dentro das regras do jogo."""
        return self._validate_group(numbers, self.config.NUMBERS_TO_SELECT)

    def validate_game(self, game: Numbers) -> bool:
        """Valida um jogo individual."""
        return self._validate_group(game, self.config.NUMBERS_PER_GAME)

    def _validate_group(self, group: Numbers, config_number) -> bool:
        """Valida um grupo de números."""
        if not group:
            return False

        if len(group) != config_number:
            return False

        if not all(self.config.MIN_NUMBER <= n <= self.config.MAX_NUMBER for n in group):
            return False

        if len(set(group)) != len(group):
            return False

        return True
