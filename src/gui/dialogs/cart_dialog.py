# src/gui/dialogs/cart_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from src.gui.base_window import BaseDialog
from src.gui.create_components import CreateComponents


class CartDialog(BaseDialog):
    def __init__(self, parent: tk.Widget, cart_names: List[str]):
        super().__init__(parent)
        self.entry = None
        self.new_cart_var = None
        self.combo = None
        self.cart_var = None
        self.cart_names = cart_names
        self._create_window("Selecionar Carrinho", 400, 200)
        self.create_widgets()
        self.result = None
        self.delete = False

        self._create_button = CreateComponents.create_button

    def create_widgets(self):
        """Cria os widgets do diálogo."""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Combobox para carrinhos existentes
        ttk.Label(main_frame, text="Selecione um carrinho existente:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )

        self.cart_var = tk.StringVar()
        self.combo = ttk.Combobox(
            main_frame,
            textvariable=self.cart_var,
            values=self.cart_names
        )
        self.combo.grid(row=1, column=0, sticky="we", pady=5)

        # Campo para novo carrinho
        ttk.Label(main_frame, text="Ou crie um novo carrinho:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )

        self.new_cart_var = tk.StringVar()
        self.entry = ttk.Entry(main_frame, textvariable=self.new_cart_var)
        self.entry.grid(row=3, column=0, sticky="we", pady=5)

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=20)

        self._create_button(
            button_frame,
            text="Confirmar",
            command=self._confirm,
            side=tk.LEFT
        )

        self._create_button(
            button_frame,
            text="Deletar",
            command=self._delete,
            side=tk.LEFT
        )

        self._create_button(
            button_frame,
            text="Cancelar",
            command=self._cancel,
            side=tk.LEFT
        )

        # Configurações de redimensionamento
        self.window.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Foco inicial
        self.combo.focus_set()

    def _confirm(self):
        """Confirma a seleção/criação do carrinho."""
        new_name = self.new_cart_var.get().strip()
        selected_cart = self.cart_var.get().strip()

        if new_name and selected_cart:
            messagebox.showwarning(
                "Aviso",
                "Por favor, escolha apenas uma opção: selecionar existente ou criar novo."
            )
            return

        if new_name:
            self.result = new_name
        elif selected_cart:
            self.result = selected_cart
        else:
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecione um carrinho existente ou crie um novo."
            )
            return

        self.window.destroy()

    def _delete(self):
        """Remove o carrinho selecionado."""
        selected_cart = self.cart_var.get().strip()
        if not selected_cart:
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecione um carrinho para deletar."
            )
            return

        self.result = selected_cart
        self.delete = True
        self.window.destroy()

    def _cancel(self):
        """Cancela a operação."""
        self.window.destroy()

    def wait_for_result(self):
        """Faz o código esperar até o diálogo ser fechado."""
        self.window.wait_window(self.window)
        return self.result
