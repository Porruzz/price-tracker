# storage/database.py

import sqlite3
from datetime import datetime
from utils.logger import log
import os

DB_PATH = "storage/productos.db"

def init_db():
    """
    Inicializa la base de datos SQLite creando la tabla 'productos' si no existe.
    """
    try:
        os.makedirs("storage", exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    precio REAL,
                    disponibilidad TEXT,
                    url TEXT,
                    fuente TEXT,
                    fecha_scraping TEXT
                );
            """)
            conn.commit()
            log("[DB] Tabla 'productos' verificada o creada exitosamente.")
    except Exception as e:
        log(f"[ERROR] No se pudo inicializar la base de datos: {e}")


def insertar_producto(producto: dict):
    """
    Inserta un producto en la base de datos.
    :param producto: Diccionario con los datos del producto scrapeado.
    """
    # Asegura que la tabla exista antes de insertar
    init_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, precio, disponibilidad, url, fuente, fecha_scraping)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                producto.get("nombre_producto"),
                producto.get("precio"),
                producto.get("disponibilidad"),
                producto.get("url"),
                producto.get("fuente"),
                producto.get("fecha_consulta")
            ))
            conn.commit()
            log(f"[DB] Producto insertado: {producto.get('nombre_producto')}")
    except Exception as e:
        log(f"[ERROR] No se pudo insertar producto en la base de datos: {e}")


def leer_productos(filtros: dict = None) -> list:
    """
    Lee productos desde la base de datos según filtros opcionales.
    :param filtros: Diccionario con filtros como fecha, fuente, etc.
    :return: Lista de diccionarios con productos.
    """
    # Asegura que la tabla exista antes de leer
    init_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM productos"
            conditions = []
            params = []

            if filtros:
                if "fuente" in filtros:
                    conditions.append("fuente = ?")
                    params.append(filtros["fuente"])
                if "fecha" in filtros:
                    conditions.append("DATE(fecha_scraping) = ?")
                    params.append(filtros["fecha"])

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY fecha_scraping DESC"
            cursor.execute(query, params)

            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        log(f"[ERROR] No se pudo leer productos desde la base de datos: {e}")
        return []