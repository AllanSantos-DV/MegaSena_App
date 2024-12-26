# src/core/combination_generator.py
from typing import List, Tuple

from .base_types import GameConfig, Numbers, Groups
from .game_validator import GameValidator


class CombinationGenerator:
    def __init__(self, config: GameConfig = GameConfig()):
        self.config = config
        self.validator = GameValidator(config)

    def split_into_groups(self, numbers: Numbers) -> Tuple[Numbers, Numbers]:
        """Divide os números em dois grupos de 6."""
        if not self.validator.validate_numbers(numbers):
            raise ValueError("Números inválidos para geração de combinações")

        return numbers[:6], numbers[6:]

    @staticmethod
    def split_group_in_three(group: Numbers) -> Tuple[Numbers, Numbers]:
        """Divide um grupo de 6 números em dois grupos de 3."""
        if len(group) != 6:
            raise ValueError("Grupo deve conter exatamente 6 números")

        return group[:3], group[3:]

    def generate_combinations(self, groups: Groups) -> List[Numbers]:
        """Gera todas as combinações possíveis entre os grupos."""
        if not groups or len(groups) < 2:
            raise ValueError("São necessários pelo menos 2 grupos para gerar combinações")

        combinations_list = []
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                combination = sorted(groups[i] + groups[j])
                if self.validator.validate_game(combination):
                    combinations_list.append(combination)

        return combinations_list

    def process_numbers(self, numbers: Numbers) -> List[Numbers]:
        """Processa os números selecionados e gera todas as combinações válidas."""
        # Divide em dois grupos de 6
        grupo1, grupo2 = self.split_into_groups(numbers)

        # Divide cada grupo de 6 em dois grupos de 3
        g1_1, g1_2 = self.split_group_in_three(grupo1)
        g2_1, g2_2 = self.split_group_in_three(grupo2)

        # Gera todas as combinações possíveis
        return self.generate_combinations([g1_1, g1_2, g2_1, g2_2])
