from dotenv import load_dotenv

load_dotenv()

import logging
import os
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    # Carrega variáveis de ambiente
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_dir = os.getenv("LOG_DIR", "logs")

    # Cria o diretório se não existir
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Caminho completo do arquivo de log
    log_file = Path(log_dir) / f"{name}.log"

    # Cria o logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Evita duplicação de handlers
    if not logger.handlers:
        # Formato do log
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para arquivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
