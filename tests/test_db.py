import unittest
from storage.database import insertar_producto, leer_productos

class TestDB(unittest.TestCase):
    def test_insertar_y_leer_producto(self):
        producto = {
            "nombre_producto": "Test Producto",
            "precio": 99.99,
            "disponibilidad": "En stock",
            "url": "https://ejemplo.com/producto-test",
            "fuente": "amazon",
            "fecha_consulta": "2025-04-22 21:00:00"
        }
        insertar_producto(producto)
        productos = leer_productos()
        self.assertTrue(any(p['url'] == producto['url'] for p in productos))

if __name__ == "__main__":
    unittest.main()
