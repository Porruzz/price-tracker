# drivers/mercadolibre.py

import requests
import time
import random
from bs4 import BeautifulSoup
from config.settings import HEADERS
from datetime import datetime


def get_mercadolibre_html(url: str, use_delay: bool = True) -> str:
    """
    Descarga el HTML de la página de producto de MercadoLibre.
    """
    try:
        if use_delay:
            time.sleep(random.uniform(1.5, 3.5))  # Simula comportamiento humano

        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else 'N/A'
        print(f"[ERROR] HTTP {status} al obtener {url}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error en la solicitud a MercadoLibre: {e}")
        return None


def parse_mercadolibre(html: str, base_url: str = None) -> dict:
    """
    Extrae nombre, precio y disponibilidad de un HTML de MercadoLibre.
    """
    soup = BeautifulSoup(html, 'html.parser')
    # Nombre del producto
    nombre_tag = soup.select_one('h1.ui-pdp-title')
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else 'Desconocido'

    # Precio del producto (parte entera + decimales)
    precio_tag = soup.select_one('span.price-tag-fraction')
    precio_text = precio_tag.get_text().replace('.', '').strip() if precio_tag else '0'
    try:
        precio = float(precio_text)
    except ValueError:
        precio = 0.0

    # Disponibilidad
    dispo_tag = soup.select_one('span.andes-tooltip__trigger')
    disponibilidad = dispo_tag.get_text(strip=True) if dispo_tag else 'Desconocida'

    return {
        'nombre_producto': nombre,
        'precio': precio,
        'disponibilidad': disponibilidad,
        'url': base_url or '',
        'fuente': 'mercadolibre',
        'fecha_consulta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }