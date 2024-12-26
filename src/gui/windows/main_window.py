# src/gui/windows/main_window.py
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List

import pandas as pd

from src.core.base_types import GameConfig
from src.data.storage_factory import StorageFactory
from src.gui.base_window import BaseWindow
from src.gui.components.number_grid import NumberGrid
from src.gui.components.ticket_viewer import TicketViewer
from src.gui.create_components import CreateComponents
from src.gui.dialogs.cart_dialog import CartDialog
from src.logging_config import logger
from src.models.selection import Selection
from src.models.ticket import Ticket


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.sequence_button = None
        self.number_grid = None
        self.main_frame = None
        self.show_mensagem = None
        self.numbers_list = None
        self._create_window("Gerador de Cartões da Mega-Sena")

        self.config = GameConfig()
        self.selection = Selection()
        self.storage = StorageFactory.get_storage("excel")
        self._create_button = CreateComponents.create_button
        self._create_label = CreateComponents.create_label

        self.create_widgets()

    def create_widgets(self):
        """Cria todos os widgets da janela principal."""
        # Frame principal
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Grade de números
        self.number_grid = NumberGrid(
            self.main_frame,
            self.config,
            self._on_number_selected
        )
        self.number_grid.grid(row=0, column=0, padx=10, pady=10)

        # Frame de ações
        action_frame = self._create_action_frame()
        action_frame.grid(row=1, column=0, padx=10, pady=10)

        # Frame de arquivo
        file_frame = self._create_file_frame()
        file_frame.grid(row=2, column=0, padx=10, pady=10)

        # Configurações de redimensionamento
        self.window.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

    def _create_action_frame(self) -> ttk.Frame:
        """Cria o frame com os botões de ação."""
        frame = ttk.Frame(self.main_frame)

        # Botões principais
        self._create_button(frame, "Gerar Cartões", self._generate_tickets, 2, 1)
        self._create_button(frame, "Preenchimento Aleatório", self._random_fill, 2, 2)
        self._create_button(frame, "Limpar Seleção", self._clear_selection, 2, 3)
        self._create_button(frame, "Visualizar Cartões", self._view_tickets, 3, 1)
        return frame

    def _create_file_frame(self) -> ttk.Frame:
        """Cria o frame com as opções de arquivo."""
        frame = ttk.Frame(self.main_frame)

        # Botão para selecionar arquivo
        self._create_button(frame, "Selecionar Arquivo XLSX", self._select_file, 4, 1)
        # Campo para coluna inicial
        self._create_label(frame, "Coluna Inicial:", 4, 2)
        self.column_entry = ttk.Entry(frame, width=5, state=tk.DISABLED)
        self.column_entry.grid(row=4, column=3, padx=5, pady=5)
        # Botão para identificar sequências
        self.sequence_button = self._create_button(
            frame, "Identificar Sequências", self._sequences_ordernadas_aparicoes, 5, 1, True)


        return frame

    def _on_number_selected(self, number: int, selected: bool):
        """Callback para quando um número é selecionado/desselecionado."""
        if selected:
            self.selection.add_number(number)
        else:
            self.selection.remove_number(number)

    def _generate_tickets(self):
        """Gera os cartões e salva no carrinho."""
        if not self.selection.is_complete():
            messagebox.showerror(
                "Erro",
                "Você deve selecionar exatamente 12 números."
            )
            return

        dialog, cart_names = self._abrir_dialogo()
        self._process_dialog(dialog, cart_names)

    def _abrir_dialogo(self):
        # Abre diálogo para selecionar/criar carrinho
        cart_names = self.storage.list_carts()
        dialog = CartDialog(self.window, cart_names)
        dialog.wait_for_result()
        self.show_mensagem = True
        return dialog, cart_names

    def _process_dialog(self, dialog, cart_names):

        try:

            if dialog.result:
                # Gera os tickets
                tickets = self.selection.generate_tickets()

                if not tickets:
                    messagebox.showerror("Erro", "Erro ao gerar tickets.")
                    return

                # Converte para formato de lista de números
                ticket_numbers = [ticket.numbers for ticket in tickets]

                # Cria o arquivo de armazenamento se não existir
                self.storage.create_storage()

                result = self.storage.add_cart(dialog.result, ticket_numbers)

                # Salva no carrinho
                if result:
                    message = (f"Cartões adicionados ao carrinho existente '{dialog.result}'"
                               if dialog.result in cart_names else
                               f"Novo carrinho '{dialog.result}' criado com os cartões")

                    if self.show_mensagem:
                        self.show_mensagem = False
                        messagebox.showinfo("Sucesso", message)
                    self._clear_selection()
                else:
                    messagebox.showerror(
                        "Erro",
                        "Não foi possível adicionar os cartões ao carrinho."
                    )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar cartões: {str(e)}")

    def _view_tickets(self):
        """Abre janela para visualizar cartões de um carrinho."""
        cart_names = self.storage.list_carts()
        if not cart_names:
            messagebox.showinfo("Aviso", "Nenhum carrinho disponível.")
            return

        dialog = CartDialog(self.window, cart_names)

        dialog.wait_for_result()

        if dialog.result:

            if dialog.delete:
                result = self.storage.delete_cart(dialog.result)
                if result:
                    messagebox.showinfo("Sucesso", f"Carrinho '{dialog.result}' removido.")
                else:
                    messagebox.showerror("Erro", "Não foi possível deletar o carrinho.")
                return

            numbers = self.storage.get_cart_tickets(dialog.result)
            if numbers:
                self._show_tickets_window(
                    [Ticket(numbers=nums) for nums in numbers]
                )
            else:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível carregar os cartões do carrinho."
                )

    def _show_tickets_window(self, tickets: List[Ticket]):
        """Exibe janela com visualizador de ‘tickets’."""
        window = tk.Toplevel(self.window)
        window.title("Visualizar Cartões")

        viewer = TicketViewer(window)
        viewer.pack(padx=10, pady=10)
        viewer.set_tickets(tickets)

    def _random_fill(self):
        """Preenche aleatoriamente os números."""
        self._clear_selection()
        available = list(range(1, 61))
        for _ in range(12):
            number = random.choice(available)
            available.remove(number)
            self.number_grid.select_number(number)

    def _clear_selection(self):
        """Limpa a seleção atual."""
        self.selection.clear()
        self.number_grid.clear_selection()

    def _select_file(self):
        """Abre diálogo para selecionar arquivo Excel."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if file_path:
            self.excel_path = file_path
            self.column_entry.config(state=tk.NORMAL)
            self.sequence_button.config(state=tk.NORMAL)

    def _sequences_ordernadas_aparicoes(self):
        """Identifica e exibe sequências no arquivo Excel."""
        self._identify_sequences()
        numbers_list = self.numbers_list

        # Conta frequência dos números
        frequency = {}
        for row in numbers_list:
            for num in row:
                frequency[num] = frequency.get(num, 0) + 1

        # Ordena números pela frequência
        numbers = list(range(1, 61))
        numbers.sort(key=lambda x: frequency.get(x, 0), reverse=True)

        # Gera 5 sequências de 12 números
        sequences = []
        current_sequence = []

        for number in numbers:
            if len(current_sequence) < 12:
                current_sequence.append(number)
            else:
                sequences.append(current_sequence)
                current_sequence = [number]

        if current_sequence:
            sequences.append(current_sequence)

        self._show_sequences(sequences[:5])  # Limita a 5 sequências

    def _identify_sequences(self):
        """Identifica e exibe sequências no arquivo Excel."""
        try:
            column = int(self.column_entry.get())

            numbers_list = self._read_excel_numbers(self.excel_path, column)

            if not numbers_list:
                messagebox.showerror("Erro", "Não foi possível ler os números do arquivo.")
                return

            self.numbers_list = numbers_list

        except ValueError:
            messagebox.showerror("Erro", "Coluna inválida.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    @staticmethod
    def _read_excel_numbers(file_path: str, column: int) -> List[List[int]]:
        """Lê números do arquivo Excel."""
        try:
            df = pd.read_excel(file_path)
            # Ajusta índice da coluna para começar do 0
            col_start = column - 1
            # Pega 6 colunas a partir da coluna inicial
            data = df.iloc[:, col_start:col_start + 6].values.tolist()
            # Filtra linhas válidas (que contém 6 números)
            return [[int(n) for n in row if not pd.isna(n)] for row in data if any(not pd.isna(x) for x in row)]
        except Exception as e:
            logger.error(f"Erro ao ler arquivo Excel: {e}")
            return []

    def _show_sequences(self, numbers_list: List[List[int]]):
        """Exibe janela com as sequências identificadas, com opção de gerar cartões."""
        window = tk.Toplevel(self.window)
        window.title("Sequências Identificadas")
        window.geometry("400x400")

        # Criar um Frame com scrollbar
        main_frame = ttk.Frame(window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista para rastrear os checkboxes
        self.sequence_selection_vars = []

        if not numbers_list:
            ttk.Label(scrollable_frame, text="Nenhuma sequência encontrada").pack(padx=10, pady=5)
        else:
            # Criar labels e checkboxes para cada sequência
            for i, sequence in enumerate(numbers_list, 1):
                sequence_var = tk.BooleanVar()
                self.sequence_selection_vars.append((sequence_var, sequence))

                frame = ttk.Frame(scrollable_frame)
                frame.pack(fill=tk.X, pady=5)

                checkbox = ttk.Checkbutton(frame, variable=sequence_var)
                checkbox.pack(side=tk.LEFT)

                sequence_str = ", ".join(map(str, sequence))
                label = ttk.Label(frame, text=f"Sequência {i}: {sequence_str}", wraplength=300)
                label.pack(side=tk.LEFT, padx=10)

        # Botão para gerar cartões
        self._create_button(
            window,
            text="Gerar Cartões",
            command=lambda: self._process_selected_sequences(window)
        ).pack(pady=10)

        # Configurar botão de fechar
        self._create_button(
            window,
            text="Fechar",
            command=window.destroy
        ).pack(pady=5)

    def _process_selected_sequences(self, window: tk.Toplevel):
        """Processa as sequências selecionadas para geração de cartões."""
        selected_sequences = [
            sequence for var, sequence in self.sequence_selection_vars if var.get()
        ]

        if not selected_sequences:
            messagebox.showwarning("Aviso", "Nenhuma sequência foi selecionada.")
            return

        try:
            # Abre diálogo para selecionar/criar carrinho
            dialog, cart_names = self._abrir_dialogo()
            for sequence in selected_sequences:
                self.selection.set_numbers(sequence)
                self._process_dialog(dialog, cart_names)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar sequências: {str(e)}")
            return

        messagebox.showinfo("Sucesso", "Cartões gerados para todas as sequências selecionadas.")
        window.destroy()
