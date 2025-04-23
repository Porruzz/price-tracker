# core/alert.py

import requests
import re
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import log

def escape_markdown(text: str) -> str:
    """
    Escapa caracteres especiales para evitar errores en Markdown (Telegram).
    """
    return re.sub(r'([_*\[\]()~`>#+=|{}.!-])', r'\\\1', text)

def verificar_alerta(producto: dict, umbral: float):
    """
    Verifica si el precio del producto está por debajo del umbral y envía una alerta por Telegram.
    :param producto: Diccionario con los datos del producto.
    :param umbral: Precio mínimo que activa una alerta.
    """
    precio = producto.get("precio")
    nombre = producto.get("nombre_producto")
    url = producto.get("url")

    log(f"[DEBUG] Producto recibido para alerta: {producto}")
    log(f"[DEBUG] Comparando precio: {precio} <= umbral: {umbral}")

    if precio is None:
        log(f"[❌] Precio no disponible para evaluar alerta: {nombre}")
        return

    if precio <= umbral:
        plataforma = "MercadoLibre" if "mercadolibre.com" in url else "Amazon"
        mensaje = f"""
🚨 *¡Alerta de Precio!*
📌 Producto: {escape_markdown(nombre)}
💲 Precio actual: ${precio}
🎯 Umbral definido: ${umbral}
🔗 [Ver producto en {plataforma}]({url})
"""
        enviado = enviar_alerta_telegram(mensaje)
        if enviado:
            log(f"[✅] Alerta enviada por Telegram: {nombre}")
        else:
            log(f"[⚠️] No se pudo enviar alerta para: {nombre}")
    else:
        log(f"[ℹ️] Sin alerta: {nombre} está en ${precio}, umbral es ${umbral}")

def enviar_alerta_telegram(mensaje: str) -> bool:
    """
    Envía un mensaje al bot de Telegram.
    :param mensaje: Mensaje a enviar (en Markdown)
    :return: True si se envió correctamente, False si hubo error
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        log(f"[DEBUG] Respuesta de Telegram: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        log(f"[❌] Error enviando a Telegram: {e}")
        return False
