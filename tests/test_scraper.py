# tests/test_scraper.py

import unittest
from core.scraper import run_scraper

class TestScraperAmazon(unittest.TestCase):
    def test_producto_invalido(self):
        producto = {
            "url": "",  # URL vacía
            "fuente": "amazon",
            "umbral": 100
        }
        resultado = run_scraper(producto)
        self.assertIsNone(resultado)

    def test_fuente_no_soportada(self):
        producto = {
            "url": "https://google.com",
            "fuente": "google",
            "umbral": 100
        }
        resultado = run_scraper(producto)
        self.assertIsNone(resultado)

if __name__ == '__main__':
    unittest.main()
