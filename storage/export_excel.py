# storage/export_excel.py
import sys, os
# añade la carpeta padre de 'core/' o 'storage/' al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
from storage.database import leer_productos
from datetime import datetime

def exportar_excel(ruta_salida: str, filtros: dict | None = None):
    """
    Lee productos según filtros y exporta todo a un archivo Excel.
    """
    productos = leer_productos(filtros)
    if not productos:
        print("🔍 No hay productos para exportar.")
        return

    df = pd.DataFrame(productos)
    df.to_excel(ruta_salida, index=False)
    print(f"✅ Exportado a Excel en: {ruta_salida}")

def main():
    parser = argparse.ArgumentParser(
        description="Exportar historial de productos a Excel."
    )
    parser.add_argument(
        "--fuente",
        choices=["amazon", "mercadolibre"],
        help="Fuente de los productos"
    )
    parser.add_argument(
        "--fecha",
        help="Fecha de scraping en formato YYYY-MM-DD"
    )
    parser.add_argument(
        "--output",
        default="storage/productos.xlsx",
        help="Ruta de salida del archivo Excel"
    )
    args = parser.parse_args()

    filtros: dict = {}
    if args.fuente:
        filtros["fuente"] = args.fuente

    if args.fecha:
        try:
            datetime.strptime(args.fecha, "%Y-%m-%d")
            filtros["fecha"] = args.fecha
        except ValueError:
            print("❌ Formato de fecha inválido. Usa YYYY-MM-DD.")
            return

    exportar_excel(args.output, filtros or None)

if __name__ == "__main__":
    main()
