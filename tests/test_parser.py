# tests/test_parser.py

import unittest
from core.parser import parse_amazon

# HTML de ejemplo simulado (podrías guardar esto en un archivo .html si crece)
HTML_MOCK = """
<html>
<head><title>Amazon Mock</title></head>
<body>
    <span id="productTitle">Producto de prueba Amazon</span>
    <span id="priceblock_ourprice">$199.99</span>
    <div id="availability"><span>In Stock</span></div>
</body>
</html>
"""

class TestParserAmazon(unittest.TestCase):
    def test_parse_html_basico(self):
        url_mock = "https://www.amazon.com/dp/B000000000"
        datos = parse_amazon(HTML_MOCK, url_mock)

        self.assertIsInstance(datos, dict)
        self.assertEqual(datos['nombre_producto'], "Producto de prueba Amazon")
        self.assertEqual(datos['precio'], 199.99)
        self.assertEqual(datos['disponibilidad'], "In Stock")
        self.assertEqual(datos['url'], url_mock)
        self.assertIn("fecha_consulta", datos)

if __name__ == '__main__':
    unittest.main()
