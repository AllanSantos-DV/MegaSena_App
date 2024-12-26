# src/gui/base_window.py
import tkinter as tk
from abc import ABC, abstractmethod


class BaseWindow(ABC):
    def __init__(self):
        self.window = None

    def _create_window(self, title: str, width: int = 600, height: int = 600):
        """Cria e configura uma janela base."""
        self.window = tk.Toplevel() if isinstance(self, BaseDialog) else tk.Tk()
        self.window.title(title)
        self.centralize_window(width, height)

    def centralize_window(self, width: int, height: int):
        """Centraliza a janela na tela."""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window.geometry(f'{width}x{height}+{x}+{y}')

    @abstractmethod
    def create_widgets(self):
        """Método abstrato para criar widgets específicos."""
        pass

    def run(self):
        """Inicia o loop principal da janela."""
        self.window.mainloop()


class BaseDialog(BaseWindow):
    def create_widgets(self):
        pass

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.result = None

    def _create_window(self, title: str, width: int = 400, height: int = 200):
        """Cria uma janela de diálogo modal."""
        super()._create_window(title, width, height)
        self.window.transient(self.parent)
        self.window.grab_set()
