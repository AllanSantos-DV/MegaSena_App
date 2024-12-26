# src/models/cart.py
from dataclasses import dataclass, field
from typing import List, Dict

from .ticket import Ticket


@dataclass
class Cart:
    name: str
    tickets: List[Ticket] = field(default_factory=list)

    def add_ticket(self, ticket: Ticket) -> None:
        """Adiciona um ‘ticket’ ao carrinho."""
        if ticket not in self.tickets:
            self.tickets.append(ticket)

    def add_tickets(self, tickets: List[Ticket]) -> None:
        """Adiciona múltiplos tickets ao carrinho."""
        for ticket in tickets:
            self.add_ticket(ticket)

    def remove_ticket(self, ticket: Ticket) -> bool:
        """Remove um ticket do carrinho."""
        if ticket in self.tickets:
            self.tickets.remove(ticket)
            return True
        return False

    def get_tickets(self) -> List[Ticket]:
        """Retorna todos os tickets do carrinho."""
        return self.tickets.copy()

    def clear(self) -> None:
        """Remove todos os ‘tickets’ do carrinho."""
        self.tickets.clear()

    def __len__(self) -> int:
        return len(self.tickets)

    def __iter__(self):
        return iter(self.tickets)

    def check_results(self, result: List[int]) -> Dict[int, List[Ticket]]:
        """
        Verifica os acertos de cada ‘ticket’ com o resultado.
        Retorna um dicionário com a quantidade de acertos como chave
        e lista de ‘tickets’ correspondente como valor.
        """
        matches = {i: [] for i in range(7)}  # 0 a 6 acertos possíveis

        for ticket in self.tickets:
            acertos = ticket.matches_with(result)
            matches[acertos].append(ticket)

        return matches
