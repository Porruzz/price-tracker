# drivers/amazon.py

import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.settings import HEADERS

def get_amazon_html(url: str, use_delay: bool = True) -> str:
    """
    Obtiene el HTML de una página de Amazon simulando comportamiento humano.
    :param url: URL de producto o búsqueda en Amazon.
    :param use_delay: Si es True, duerme un intervalo aleatorio antes de la petición.
    :return: HTML de la página o None si falla.
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
        print(f"[ERROR] Error en la solicitud a Amazon: {e}")
        return None


def parse_amazon(html: str, base_url: str = None) -> dict:
    """
    Extrae información de producto de un HTML de Amazon.
    :param html: HTML devuelto por get_amazon_html.
    :param base_url: URL original para referencia.
    :return: Diccionario con nombre_producto, precio, disponibilidad, url, fuente, fecha_consulta.
    """
    soup = BeautifulSoup(html, 'html.parser')
    # Nombre del producto
    nombre_tag = soup.select_one('#productTitle')
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else 'Desconocido'

    # Precio del producto
    precio_tag = soup.select_one('#priceblock_ourprice, #priceblock_dealprice')
    precio_text = precio_tag.get_text().strip().replace('$', '').replace(',', '') if precio_tag else '0'
    try:
        precio = float(precio_text)
    except ValueError:
        precio = 0.0

    # Disponibilidad (stock)
    dispo_tag = soup.select_one('#availability .a-color-state, #availability .a-color-success')
    disponibilidad = dispo_tag.get_text(strip=True) if dispo_tag else 'No disponible'

    return {
        'nombre_producto': nombre,
        'precio': precio,
        'disponibilidad': disponibilidad,
        'url': base_url or '',
        'fuente': 'amazon',
        'fecha_consulta': time.strftime('%Y-%m-%d %H:%M:%S')
    }