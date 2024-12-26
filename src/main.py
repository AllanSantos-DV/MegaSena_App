#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

from src.logging_config import logger

# Adiciona o diretório src ao PYTHON_PATH
sys.path.append(str(Path(__file__).parent))

from src.gui import MainWindow

def main():
    """Função principal da aplicação."""

    try:
        # Garante que a pasta logs existe para armazenamento
        data_dir = Path("logs")
        data_dir.mkdir(exist_ok=True)

        logger.info("Iniciando aplicação...")
        # Garante que a pasta data existe para armazenamento
        data_dir = Path("xlsx")
        data_dir.mkdir(exist_ok=True)

        # Inicia a interface gráfica
        app = MainWindow()
        app.run()

    except Exception as e:
        logger.error(f"Erro fatal na aplicação: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()