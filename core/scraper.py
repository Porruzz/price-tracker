# core/scraper.py

from drivers.amazon import get_amazon_html
from drivers.mercadolibre import get_mercadolibre_html
from core.parser import parse_amazon, parse_mercadolibre
from core.alert import verificar_alerta
from utils.logger import log


def run_scraper(product: dict) -> dict:
    """
    Orquesta el scraping de un producto según su fuente.
    :param product: dict con 'url', 'fuente' y opcional 'umbral'
    :return: dict con datos estructurados o None si falla
    """
    url = product.get("url")
    fuente = product.get("fuente")
    umbral = product.get("umbral", 999999)

    # Normalizar URL si empieza con 'www.'
    if url and url.startswith("www."):
        url = "https://" + url
        log(f"[INFO] URL normalizada con https://: {url}")

    if not url or not fuente:
        log("[ERROR] Faltan datos del producto: 'url' o 'fuente'")
        return None

    # Selección de driver según la fuente
    if fuente.lower() == "amazon":
        html = get_amazon_html(url)
        if not html:
            log(f"[ERROR] No se pudo obtener HTML desde Amazon: {url}")
            return None
        datos = parse_amazon(html, url)

    elif fuente.lower() == "mercadolibre":
        html = get_mercadolibre_html(url)
        if not html:
            log(f"[ERROR] No se pudo obtener HTML desde MercadoLibre: {url}")
            return None
        datos = parse_mercadolibre(html, url)

    else:
        log(f"[ERROR] Fuente no soportada: {fuente}")
        return None

    # Validación de datos extraídos
    if not datos or not datos.get("nombre_producto") or datos.get("precio") is None:
        log("[ERROR] Datos incompletos o inválidos.")
        return None

    # Verificar y enviar alerta si corresponde
    verificar_alerta(datos, umbral)
    return datos
