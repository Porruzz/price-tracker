# utils/logger.py

import os
import logging

# Crear carpeta si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configurar logging
log_file = os.path.join(LOG_DIR, "scraper.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(message: str, level="info"):
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    elif level == "warn":
        logging.warning(message)
    else:
        logging.debug(message)
