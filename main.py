# main.py

import os
import tempfile
import time
import argparse
import sys
from datetime import datetime

from core.scraper import run_scraper
from storage.export_csv import exportar_a_csv
from storage.export_excel import exportar_excel
from storage.database import init_db, insertar_producto, leer_productos
from config.settings import LOG_FILE


def limpiar_archivos_temporales(dias: int = 3):
    """
    Elimina archivos *_debug_*.html en la carpeta temporal con más de 'dias' días de antigüedad.
    """
    temp_dir = tempfile.gettempdir()
    ahora = time.time()

    for archivo in os.listdir(temp_dir):
        if "_debug_" in archivo and archivo.endswith(".html"):
            ruta = os.path.join(temp_dir, archivo)
            try:
                if os.path.isfile(ruta):
                    edad_dias = (ahora - os.path.getmtime(ruta)) / (60 * 60 * 24)
                    if edad_dias > dias:
                        os.remove(ruta)
                        print(f"[INFO] 🧹 Eliminado archivo temporal antiguo: {archivo}")
            except Exception as e:
                print(f"[WARN] No se pudo eliminar {archivo}: {e}")


def limpiar_logs_antiguos(dias: int = 7):
    """
    Elimina logs que tengan más de 'dias' días desde la última modificación.
    """
    if not os.path.exists(LOG_FILE):
        return
    ahora = time.time()
    try:
        edad_dias = (ahora - os.path.getmtime(LOG_FILE)) / (60 * 60 * 24)
        if edad_dias > dias:
            os.remove(LOG_FILE)
            print(f"[INFO] 🧹 Log eliminado por antigüedad: {LOG_FILE}")
    except Exception as e:
        print(f"[WARN] No se pudo eliminar el log: {e}")


def cmd_run(args):
    """
    Subcomando 'run': modo interactivo. Pide URLs, scrapea, guarda en BD y genera CSV.
    """
    init_db()
    limpiar_archivos_temporales()
    limpiar_logs_antiguos()

    print("=" * 60)
    print("📦 Price Tracker - Scraper de Amazon y MercadoLibre")
    print("=" * 60)

    productos_scrapeados = []
    while True:
        url = input("\n🔗 Ingresa la URL del producto (o escribe 'salir'): ").strip()
        if url.lower() == "salir":
            break
        if not url.startswith("http"):
            print("❌ URL inválida. Asegúrate de que comience con 'http'.")
            continue
        fuente = "mercadolibre" if "mercadolibre.com" in url else "amazon"
        producto = {"url": url, "fuente": fuente, "umbral": args.umbral}

        print("\n🔍 Procesando producto...\n")
        datos = run_scraper(producto)
        if datos:
            insertar_producto(datos)
            productos_scrapeados.append(datos)
            print("✅ Producto extraído exitosamente:")
            print(f"📌 Nombre: {datos['nombre_producto']}")
            print(f"💲 Precio: {datos['precio']}")
            print(f"📦 Disponibilidad: {datos['disponibilidad']}")
            print(f"🔗 URL: {datos['url']}")
            print(f"🕒 Fecha: {datos['fecha_consulta']}")
        else:
            print("❌ No se pudo obtener información del producto.")

    if productos_scrapeados:
        exportar_a_csv(productos_scrapeados)
        print(f"\n🟢 Run completado: {len(productos_scrapeados)} productos guardados y CSV generado.")
    else:
        print("\n⚠️  No se procesó ningún producto.")


def cmd_historico(args):
    """
    Subcomando 'historico': muestra historial desde la BD con filtros opcionales.
    """
    init_db()
    filtros = {}
    if args.fuente:
        filtros["fuente"] = args.fuente
    if args.fecha:
        filtros["fecha"] = args.fecha

    resultados = leer_productos(filtros or None)
    if not resultados:
        print("🔍 No se encontraron productos con esos filtros.")
        return

    from tabulate import tabulate
    tabla = [[r["id"], r["nombre"], r["precio"], r["fuente"], r["fecha_scraping"]] for r in resultados]
    print(
        tabulate(
            tabla,
            headers=["ID","Nombre","Precio","Fuente","Fecha"],
            tablefmt="fancy_grid"
        )
    )


def cmd_export(args):
    """
    Subcomando 'export': exporta histórico filtrado a Excel.
    """
    init_db()
    filtros = {}
    if args.fuente:
        filtros["fuente"] = args.fuente
    if args.fecha:
        filtros["fecha"] = args.fecha
    exportar_excel(args.output, filtros or None)


def main():
    parser = argparse.ArgumentParser(prog="price_tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # run solo en modo interactivo
    p_run = sub.add_parser("run", help="Pide URLs, scrapea y guarda (BD + CSV)")
    p_run.add_argument(
        "--umbral", type=float, default=1e9,
        help="Umbral de precio para alertas"
    )

    # histórico
    p_h = sub.add_parser("historico", help="Muestra historial de la BD")
    p_h.add_argument("--fuente", choices=["amazon","mercadolibre"])
    p_h.add_argument("--fecha", help="YYYY-MM-DD")

    # export
    p_e = sub.add_parser("export", help="Exporta histórico a Excel")
    p_e.add_argument("--fuente", choices=["amazon","mercadolibre"])
    p_e.add_argument("--fecha", help="YYYY-MM-DD")
    p_e.add_argument(
        "--output", default="storage/productos.xlsx",
        help="Ruta de salida para el archivo Excel"
    )

    args = parser.parse_args()
    if args.cmd == "run":
        cmd_run(args)
    elif args.cmd == "historico":
        cmd_historico(args)
    elif args.cmd == "export":
        cmd_export(args)

if __name__ == "__main__":
    main()