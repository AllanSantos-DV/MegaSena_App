import tkinter as tk

from ttkbootstrap import ttk


class CreateComponents:
    def __init__(self, master):
        self.master = master

    @staticmethod
    def create_button(frame, text, command, row=None, column=None, disabled=False, width=20, side=None):
        """Cria um botão e o adiciona ao frame."""
        button = ttk.Button(frame, text=text, command=command, width=width,
                            state=tk.DISABLED if disabled else tk.NORMAL)
        if row and column:
            button.grid(row=row, column=column, padx=5, pady=5)
        if side:
            button.pack(side=side, padx=5)
        return button

    @staticmethod
    def create_label(frame, text, row, column):
        """Cria um label e o adiciona ao frame."""
        label = ttk.Label(frame, text=text)
        label.grid(row=row, column=column, padx=5, pady=5)
        return label
