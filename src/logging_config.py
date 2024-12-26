import logging
import sys


def setup_logging():
    """Configura o sistema de logging da aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/megasena.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


# Configura o logging ao importar este módulo
setup_logging()
logger = logging.getLogger(__name__)
