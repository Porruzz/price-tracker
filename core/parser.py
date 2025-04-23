# core/parser.py

"""
Parser central que enruta al parser específico de cada fuente.
"""
from core.parsers.amazon_parser import parse_amazon
from core.parsers.mercadolibre_parser import parse_mercadolibre

# Mapeo de fuentes a la función de parseo correspondiente
PARSERS = {
    "amazon": parse_amazon,
    "mercadolibre": parse_mercadolibre,
}

def parse_producto(fuente: str, html: str, url: str) -> dict:
    """
    Enruta al parser específico según la fuente (amazon, mercadolibre, etc.)
    :param fuente: Nombre de la fuente ('amazon' o 'mercadolibre')
    :param html:      HTML completo de la página de producto
    :param url:       URL original del producto
    :return:          Diccionario con datos extraídos del producto
    """
    parser_func = PARSERS.get(fuente.lower())
    if not parser_func:
        raise ValueError(f"[ERROR] Fuente de parser no soportada: {fuente}")
    # Llamada al parser específico, manteniendo todos los detalles computacionales
    datos = parser_func(html, url)
    return datos
