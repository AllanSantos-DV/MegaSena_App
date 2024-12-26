# src/gui/components/ticket_viewer.py
import tkinter as tk
from tkinter import ttk
from typing import List, Optional

from src.models.ticket import Ticket


class TicketViewer(ttk.Frame):
    def __init__(self, master: tk.Toplevel):
        super().__init__(master)
        self.tickets: List[Ticket] = []
        self.current_index = 0

        self._create_widgets()

    def _create_widgets(self):
        """Cria os widgets do visualizador."""
        # Frame para exibir os números do ticket
        self.ticket_frame = ttk.Frame(self)
        self.ticket_frame.grid(row=0, column=0, padx=10, pady=10)

        # Frame para navegação
        nav_frame = ttk.Frame(self)
        nav_frame.grid(row=1, column=0, padx=10, pady=10)

        # Botões de navegação
        self.prev_button = ttk.Button(
            nav_frame,
            text="<",
            command=self.previous_ticket,
            width=5
        )
        self.prev_button.grid(row=0, column=0, padx=5)

        self.ticket_counter = ttk.Label(nav_frame, text="0/0")
        self.ticket_counter.grid(row=0, column=1, padx=10)

        self.next_button = ttk.Button(
            nav_frame,
            text=">",
            command=self.next_ticket,
            width=5
        )
        self.next_button.grid(row=0, column=2, padx=5)

        # Total de tickets
        self.total_label = ttk.Label(nav_frame, text="Total: 0")
        self.total_label.grid(row=1, column=0, columnspan=3, pady=10)

    def _update_display(self):
        """Atualiza a exibição do ‘ticket’ atual."""
        # Limpa o frame do ticket
        for widget in self.ticket_frame.winfo_children():
            widget.destroy()

        if not self.tickets:
            return

        # Exibe o ticket atual
        ticket = self.tickets[self.current_index]
        for i, number in enumerate(ticket.numbers):
            ttk.Label(
                self.ticket_frame,
                text=str(number),
                width=5
            ).grid(row=0, column=i, padx=5)

        # Atualiza contador
        self.ticket_counter["text"] = f"{self.current_index + 1}/{len(self.tickets)}"
        self.total_label["text"] = f"Total: {len(self.tickets)}"

        # Atualiza estado dos botões
        self.prev_button["state"] = "normal" if self.current_index > 0 else "disabled"
        self.next_button["state"] = "normal" if self.current_index < len(self.tickets) - 1 else "disabled"

    def set_tickets(self, tickets: List[Ticket]):
        """Define a lista de ‘tickets’ para exibição."""
        self.tickets = tickets
        self.current_index = 0 if tickets else -1
        self._update_display()

    def next_ticket(self):
        """Avança para o próximo ‘ticket’."""
        if self.current_index < len(self.tickets) - 1:
            self.current_index += 1
            self._update_display()

    def previous_ticket(self):
        """Volta para o ticket anterior."""
        if self.current_index > 0:
            self.current_index -= 1
            self._update_display()

    def get_current_ticket(self) -> Optional[Ticket]:
        """Retorna o ticket atual ou None se não houver tickets."""
        if not self.tickets or self.current_index < 0:
            return None
        return self.tickets[self.current_index]
