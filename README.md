<<<<<<< HEAD

# 📈 Price Tracker - Rastreador de Precios en Amazon y MercadoLibre

Un sistema de scraping automatizado que rastrea el precio de productos en **Amazon** y **MercadoLibre**, guarda los datos en una base de datos **SQLite**, y permite exportarlos o consultarlos fácilmente desde la consola.  
Ideal para vendedores, compradores inteligentes o desarrolladores que desean automatizar análisis de precios.

---

## 🛠️ Tecnologías Usadas

- **Python 3.10+**
- `requests`, `beautifulsoup4`
- `sqlite3`, `pandas`, `tabulate`, `openpyxl`
- CLI interactiva (`argparse`)
- Automatizable por cron (Linux) o Task Scheduler (Windows)

---

## 📂 Estructura del Proyecto

```
price-tracker/
│
├── config/             # Configuraciones globales
├── core/               # Lógica del scraper, parsers y alertas
├── drivers/            # HTML scrapers para Amazon y MercadoLibre
├── storage/            # Conexión y consultas a la base de datos SQLite
├── outputs/            # Exportaciones CSV / Excel
├── utils/              # Logs y funciones auxiliares
├── tests/              # Pruebas automáticas
│
├── main.py             # CLI principal del sistema
├── requirements.txt    # Dependencias del entorno virtual
├── README.md           # Este documento
```

---

## 🚀 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Porruzz/price-tracker.git
cd price-tracker
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
venv\Scripts\activate    # En Windows
source venv/bin/activate   # En Linux/macOS
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 🧠 ¿Qué hace este proyecto?

- Extrae el **nombre**, **precio** y **disponibilidad** de productos.
- Guarda el historial de precios en `storage/precios.db`.
- Notifica si el precio baja por debajo de un umbral definido.
- Permite ver el historial y exportar los datos a Excel o CSV.

---

## 📌 Comandos principales

### 1. Ejecutar el Scraper
```bash
python main.py run
```
- Te pedirá una URL y extraerá automáticamente la información.

### 2. Ver historial de precios
```bash
python main.py historico
```
- Filtra por fuente, nombre o fecha.

### 3. Exportar datos
```bash
python main.py export --formato excel
python main.py export --formato csv
```

---

## 🧪 Pruebas Automáticas

Desde la raíz del proyecto:

```bash
pytest tests/
```

- Verifica que la base de datos funcione correctamente.
- Testea la estructura de un producto válido.

---

## 💡 Ejemplo de uso

```bash
python main.py run
# Pega una URL de Amazon o MercadoLibre
```

📦 Resultado:
- Producto guardado en la base de datos.
- Historial disponible con `main.py historico`.
- Exportable a Excel desde `main.py export`.

---

## 👨‍💻 Autor

**Santiago Parra Acuña**  
GitHub: [@Porruzz](https://github.com/Porruzz)  
Correo: porruzzzz@gmail.com

---

## 🖼️ Capturas sugeridas para tu portafolio

- Scraper corriendo en consola
- Exportaciones funcionando
- Vista del historial en consola
- Base de datos abierta en DB Browser
=======

# 📈 Price Tracker - Rastreador de Precios en Amazon y MercadoLibre

Un sistema de scraping automatizado que rastrea el precio de productos en **Amazon** y **MercadoLibre**, guarda los datos en una base de datos **SQLite**, y permite exportarlos o consultarlos fácilmente desde la consola.  
Ideal para vendedores, compradores inteligentes o desarrolladores que desean automatizar análisis de precios.

---

## 🛠️ Tecnologías Usadas

- **Python 3.10+**
- `requests`, `beautifulsoup4`
- `sqlite3`, `pandas`, `tabulate`, `openpyxl`
- CLI interactiva (`argparse`)
- Automatizable por cron (Linux) o Task Scheduler (Windows)

---

## 📂 Estructura del Proyecto

```
price-tracker/
│
├── config/             # Configuraciones globales
├── core/               # Lógica del scraper, parsers y alertas
├── drivers/            # HTML scrapers para Amazon y MercadoLibre
├── storage/            # Conexión y consultas a la base de datos SQLite
├── outputs/            # Exportaciones CSV / Excel
├── utils/              # Logs y funciones auxiliares
├── tests/              # Pruebas automáticas
│
├── main.py             # CLI principal del sistema
├── requirements.txt    # Dependencias del entorno virtual
├── README.md           # Este documento
```

---

## 🚀 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Porruzz/price-tracker.git
cd price-tracker
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
venv\Scripts\activate    # En Windows
source venv/bin/activate   # En Linux/macOS
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 🧠 ¿Qué hace este proyecto?

- Extrae el **nombre**, **precio** y **disponibilidad** de productos.
- Guarda el historial de precios en `storage/precios.db`.
- Notifica si el precio baja por debajo de un umbral definido.
- Permite ver el historial y exportar los datos a Excel o CSV.

---

## 📌 Comandos principales

### 1. Ejecutar el Scraper
```bash
python main.py run
```
- Te pedirá una URL y extraerá automáticamente la información.

### 2. Ver historial de precios
```bash
python main.py historico
```
- Filtra por fuente, nombre o fecha.

### 3. Exportar datos
```bash
python main.py export --formato excel
python main.py export --formato csv
```

---

## 🧪 Pruebas Automáticas

Desde la raíz del proyecto:

```bash
pytest tests/
```

- Verifica que la base de datos funcione correctamente.
- Testea la estructura de un producto válido.

---

## 💡 Ejemplo de uso

```bash
python main.py run
# Pega una URL de Amazon o MercadoLibre
```

📦 Resultado:
- Producto guardado en la base de datos.
- Historial disponible con `main.py historico`.
- Exportable a Excel desde `main.py export`.

---

## 👨‍💻 Autor

**Santiago Parra Acuña**  
GitHub: [@Porruzz](https://github.com/Porruzz)  
Correo: porruzzzz@gmail.com

---

## 🖼️ Capturas sugeridas para tu portafolio

- Scraper corriendo en consola
- Exportaciones funcionando
- Vista del historial en consola
- Base de datos abierta en DB Browser
>>>>>>> f0dde63b49963470e682147f68dcfd1cb8ff12c7
