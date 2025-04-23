import unittest
from core.parser import parse_producto

class TestValidacionProducto(unittest.TestCase):
    def test_estructura_minima(self):
        html_fake = "<html><span id='productTitle'>Fake Product</span><span class='a-offscreen'>$12.99</span><span class='a-size-medium a-color-success'>In Stock</span></html>"
        resultado = parse_producto("amazon", html_fake, "https://fake.com")
        self.assertIn("nombre_producto", resultado)
        self.assertIn("precio", resultado)
        self.assertIn("disponibilidad", resultado)
        self.assertIn("fecha_consulta", resultado)

if __name__ == "__main__":
    unittest.main()
