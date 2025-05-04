import sqlite3
from utils.logger import log

DB_PATH = "storage/productos.db"

def insertar_producto(producto: dict):
    """
    Inserta los datos del producto en la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO productos (nombre, precio, disponibilidad, url, fuente, fecha_scraping)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            producto["nombre_producto"],
            producto["precio"],
            producto["disponibilidad"],
            producto["url"],
            producto["fuente"],
            producto["fecha_consulta"]
        ))

        conn.commit()
        conn.close()
        log(f"[DB] Producto guardado en la base de datos: {producto['nombre_producto']}")

    except Exception as e:
        log(f"[ERROR] No se pudo guardar en la base de datos: {e}")
