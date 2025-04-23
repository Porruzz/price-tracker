# storage/export_csv.py

import pandas as pd
import os
from datetime import datetime

def exportar_a_csv(productos: list, carpeta_salida: str = "outputs") -> str:
    """
    Exporta una lista de productos a un archivo CSV en la carpeta de salida.
    El archivo se nombra como productos_YYYY-MM-DD.csv
    :param productos: lista de diccionarios con datos estructurados
    :param carpeta_salida: carpeta donde guardar el archivo
    :return: ruta completa del archivo generado
    """
    if not productos:
        print("[⚠️ WARN] No se exportó ningún producto porque la lista está vacía.")
        return ""

    try:
        # Asegurarse de que exista la carpeta de salida
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)
            print(f"[📁] Carpeta creada: {carpeta_salida}")

        # Nombre del archivo con fecha
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"productos_{fecha_actual}.csv"
        ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

        # Crear DataFrame y exportar
        df = pd.DataFrame(productos)
        df.to_csv(ruta_archivo, index=False, encoding='utf-8-sig')

        print(f"[✅] Productos exportados correctamente a: {ruta_archivo}")
        return ruta_archivo

    except Exception as e:
        print(f"[❌ ERROR] No se pudo exportar a CSV: {e}")
        return ""
