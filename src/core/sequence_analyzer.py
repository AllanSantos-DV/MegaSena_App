# src/core/sequence_analyzer.py
from collections import Counter
from typing import List, Dict

from .base_types import Numbers, GameConfig


class SequenceAnalyzer:
    def __init__(self, config: GameConfig = GameConfig()):
        self.config = config

    @staticmethod
    def count_number_frequency(games: List[Numbers]) -> Dict[int, int]:
        """Conta a frequência de cada número nos jogos."""
        counter = Counter()
        for game in games:
            counter.update(game)
        return dict(counter)

    def identify_sequences(self, games: List[Numbers], min_sequence_length: int = 12) -> List[Numbers]:
        """Identifica sequências de números mais frequentes."""
        frequency = self.count_number_frequency(games)
        numbers = list(range(self.config.MIN_NUMBER, self.config.MAX_NUMBER + 1))
        numbers.sort(key=lambda x: frequency.get(x, 0), reverse=True)

        sequences = []
        current_sequence = []

        for number in numbers:
            if len(current_sequence) < min_sequence_length:
                current_sequence.append(number)
            else:
                sequences.append(current_sequence)
                current_sequence = [number]

        if current_sequence:
            sequences.append(current_sequence)

        return sequences
