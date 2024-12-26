# src/gui/components/number_grid.py
import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List

from src.core.base_types import GameConfig
from src.gui.create_components import CreateComponents


class NumberGrid(ttk.Frame):
    def __init__(
            self,
            master: tk.Widget,
            config: GameConfig = GameConfig(),
            on_number_selected: Callable[[int, bool], None] = None
    ):
        super().__init__(master)
        self.config = config
        self.on_number_selected = on_number_selected
        self.buttons: Dict[int, ttk.Button] = {}
        self.selected_numbers: List[int] = []
        self._create_button = CreateComponents.create_button

        self._create_grid()

    def _create_grid(self):
        """Cria a grade de números."""
        for i, number in enumerate(range(self.config.MIN_NUMBER, self.config.MAX_NUMBER + 1)):
            button = self._create_button(
                self,
                text=str(number),
                command=lambda n=number: self._handle_number_click(n),
                width=4
            )

            button.grid(
                row=i // 10,
                column=i % 10,
                padx=2,
                pady=2
            )
            self.buttons[number] = button

    def _handle_number_click(self, number: int):
        """Manipula o clique num número."""
        if number in self.selected_numbers:
            self.deselect_number(number)
        elif len(self.selected_numbers) < self.config.NUMBERS_TO_SELECT:
            self.select_number(number)

    def select_number(self, number: int):
        """Seleciona um número."""
        if number not in self.selected_numbers and len(self.selected_numbers) < self.config.NUMBERS_TO_SELECT:
            self.selected_numbers.append(number)
            self.buttons[number].state(['pressed'])
            if self.on_number_selected:
                self.on_number_selected(number, True)

    def deselect_number(self, number: int):
        """Remove a seleção de um número."""
        if number in self.selected_numbers:
            self.selected_numbers.remove(number)
            self.buttons[number].state(['!pressed'])
            if self.on_number_selected:
                self.on_number_selected(number, False)

    def clear_selection(self):
        """Limpa todas as seleções."""
        for number in self.selected_numbers.copy():
            self.deselect_number(number)

    def get_selected_numbers(self) -> List[int]:
        """Retorna a lista de números selecionados."""
        return self.selected_numbers.copy()
