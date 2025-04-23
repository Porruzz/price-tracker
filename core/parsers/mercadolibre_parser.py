from bs4 import BeautifulSoup
from datetime import datetime
import re
import tempfile
from uuid import uuid4
from config.settings import DEBUG_MODE

def parse_mercadolibre(html: str, url: str) -> dict:
    """
    Parsea el HTML de una página de producto de MercadoLibre y extrae:
    - Nombre del producto
    - Precio
    - Disponibilidad
    - Fecha y URL de consulta
    """
    soup = BeautifulSoup(html, 'html.parser')

    nombre = "No disponible"
    precio = None
    disponibilidad = "No especificado"

    # === 1. Extraer nombre del producto ===
    posibles_selectores_nombre = [
        "h1.ui-pdp-title",
        "h1.andes-visually-hidden",
        "meta[property='og:title']",
        "title"
    ]

    for selector in posibles_selectores_nombre:
        tag = soup.select_one(selector)
        if tag:
            nombre = tag.get("content", "").strip() if tag.name == "meta" else tag.get_text(strip=True)
            if nombre:
                break

    if nombre == "No disponible":
        print("[WARN] No se encontró el nombre del producto.")
        _guardar_html_temporal(html, "ml_nombre")

    # === 2. Extraer precio del producto ===
    posibles_selectores_precio = [
        ("span.andes-money-amount__fraction", "span.andes-money-amount__cents"),
        ("div.price-tag-fraction", "div.price-tag-cents"),
        ("span.price-tag-fraction", "span.price-tag-cents")
    ]

    for sel_entero, sel_centavos in posibles_selectores_precio:
        entero = soup.select_one(sel_entero)
        centavos = soup.select_one(sel_centavos)

        if entero:
            precio_texto = entero.get_text(strip=True)
            if centavos:
                precio_texto += "," + centavos.get_text(strip=True)
            precio = _limpiar_precio(precio_texto)
            if precio:
                break

    # 🔁 Fallback adicional para tarjetas como carros/motos
    if precio is None:
        posibles_spans = soup.select("div.poly-component__price span")
        for span in posibles_spans:
            texto = span.get_text(strip=True)
            if texto and re.search(r'\d', texto):
                precio = _limpiar_precio(texto)
                if precio:
                    break

    if precio is None:
        print("[WARN] No se pudo extraer el precio del producto.")
        _guardar_html_temporal(html, "ml_precio")

    # === 3. Extraer disponibilidad ===
    disponibilidad_tag = soup.select_one(
        "span.ui-pdp-stock-information, span.ui-pdp-buybox__quantity__available, span.ui-pdp-buybox__stock__available"
    )
    if disponibilidad_tag:
        disponibilidad = disponibilidad_tag.get_text(strip=True)
    else:
        disponibilidad = "Verificar disponibilidad manualmente"

    # === 4. Fecha actual ===
    fecha_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        "nombre_producto": nombre,
        "precio": precio,
        "disponibilidad": disponibilidad,
        "url": url,
        "fecha_consulta": fecha_consulta
    }

def _limpiar_precio(texto_precio: str) -> float:
    limpio = re.sub(r'[^\d.,]', '', texto_precio)

    if limpio.count('.') > 1:
        limpio = limpio.replace('.', '')

    if ',' in limpio and '.' not in limpio:
        limpio = limpio.replace(',', '.')

    try:
        return float(limpio)
    except ValueError:
        return None

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
