import re
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
import tempfile
from uuid import uuid4
from config.settings import DEBUG_MODE
from utils.logger import log


def parse_amazon(html: str, url: str) -> dict:
    """
    Extrae título, precio y disponibilidad desde el HTML de una página de Amazon.
    Incluye delay aleatorio para simular comportamiento humano.
    """

    # Simula comportamiento humano
    time.sleep(random.uniform(1.0, 2.0))

    soup = BeautifulSoup(html, 'html.parser')

    # === 1. Nombre del producto (más robusto) ===
    nombre_tag = soup.select_one('#productTitle') or \
                 soup.select_one('span.a-size-large.product-title-word-break') or \
                 soup.select_one('h1 span')

    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "No disponible"

    if nombre == "No disponible":
        log("[WARN] No se encontró el nombre del producto.")
        _guardar_html_temporal(html, "amazon_nombre")

    # === 2. Precio ===
    precio = None
    price_text = ""

    price_tag = soup.select_one('#priceblock_ourprice, #priceblock_dealprice')
    if price_tag:
        price_text = price_tag.get_text(strip=True)
    else:
        off = soup.select_one('span.a-offscreen')
        price_text = off.get_text(strip=True) if off else ""

    if price_text:
        m = re.search(r'[\d,.]+', price_text)
        if m:
            num = m.group(0).replace(',', '')
            try:
                precio = float(num)
            except ValueError:
                log(f"[WARN] Falló conversión de precio: '{num}'")

    if precio is None:
        log("[WARN] No se pudo extraer el precio del producto.")
        _guardar_html_temporal(html, "amazon_precio")

    # === 3. Disponibilidad ===
    stock_tag = soup.select_one('span.a-size-medium.a-color-success')
    disponibilidad = stock_tag.get_text(strip=True) if stock_tag else "Verificar manualmente"

    # === 4. Fecha ===
    fecha_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        "nombre_producto": nombre,
        "precio": precio,
        "disponibilidad": disponibilidad,
        "url": url,
        "fuente": "amazon",
        "fecha_consulta": fecha_consulta
    }


def _guardar_html_temporal(html: str, motivo: str):
    if not DEBUG_MODE:
        return

    try:
        nombre_temp = f"{motivo}_debug_{uuid4().hex[:8]}.html"
        ruta_temp = tempfile.gettempdir() + "/" + nombre_temp
        with open(ruta_temp, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[DEBUG] HTML guardado temporalmente en: {ruta_temp}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar HTML temporal: {e}")
