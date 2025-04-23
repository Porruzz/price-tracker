# config/settings.py

from datetime import datetime
import os

# ==========================================
# 🌐 CABECERAS PARA REQUESTS HTTP
# ------------------------------------------
# Usa un User‑Agent válido para evitar bloqueos por parte de Amazon/MercadoLibre.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8"
}

# ==========================================
# 💬 CONFIGURACIÓN DE TELEGRAM
# ------------------------------------------
TELEGRAM_TOKEN   = "7420368913:AAH6jBXcdRSB7tYkzLiVfi-LzjrQFwbYCxU"
TELEGRAM_CHAT_ID = "6222208585"

# ==========================================
# 📁 RUTA DE EXPORTACIÓN DE CSV
# ------------------------------------------
CARPETA_EXPORTACION = "outputs"

# ==========================================
# 🧪 MODO DE DEPURACIÓN TEMPORAL (DEBUG)
# ------------------------------------------
DEBUG_MODE = True  # Cambia a False para desactivar la depuración

# ==========================================
# 📝 ARCHIVO DE LOG DEL SISTEMA
# ------------------------------------------
LOG_FILE = os.path.join("logs", "scraper.log")

# ==========================================
# 🕒 FUNCION AUXILIAR PARA NOMBRE DE ARCHIVO CSV CON FECHA
# ------------------------------------------
def nombre_csv_con_fecha() -> str:
    """
    Retorna un nombre de archivo basado en la fecha actual.
    Ej: productos_2025-03-31.csv
    """
    return f"productos_{datetime.now().strftime('%Y-%m-%d')}.csv"
