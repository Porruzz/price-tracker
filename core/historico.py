# core/historico.py
import sys, os
# añade la carpeta padre de 'core/' o 'storage/' al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from storage.database import leer_productos
from tabulate import tabulate  # pip install tabulate
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description="Visualizar historial de productos scrapeados."
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
    args = parser.parse_args()

    filtros = {}
    if args.fuente:
        filtros["fuente"] = args.fuente

    if args.fecha:
        # Validación de formato YYYY-MM-DD
        try:
            datetime.strptime(args.fecha, "%Y-%m-%d")
            filtros["fecha"] = args.fecha
        except ValueError:
            print("❌ Formato de fecha inválido. Usa YYYY-MM-DD.")
            return

    # Si no hay filtros, pasar None para leer_todos
    productos = leer_productos(filtros or None)

    if not productos:
        print("🔍 No se encontraron productos con esos filtros.")
        return

    tabla = [
        [p["id"], p["nombre"], p["precio"], p["fuente"], p["fecha_scraping"]]
        for p in productos
    ]

    print(
        tabulate(
            tabla,
            headers=["ID", "Nombre", "Precio", "Fuente", "Fecha"],
            tablefmt="fancy_grid"
        )
    )

if __name__ == "__main__":
    main()
