import unittest
import time
from taximeter import Taximeter

class TestTaximeter(unittest.TestCase):
    
    def test_calculate_fare_default_prices(self):
        tm = Taximeter()
        tm.stopped_time = 10    # 10s parado
        tm.moving_time = 20     # 20s en movimiento
        expected_fare = (10 * 0.02) + (20 * 0.05)   # 0.2 + 1.0 = 1.2
        self.assertAlmostEqual(tm.calculate_fare(), expected_fare, places=2)
        
    def test_calculate_fare_custom_prices(self):
        tm = Taximeter()
        tm.price_stopped = 0.1
        tm.price_moving = 0.2
        tm.stopped_time = 5
        tm.moving_time = 10
        expected_fare = (5 * 0.1) + (10 * 0.2)  # 0.5 + 2.0 = 2.5
        self.assertAlmostEqual(tm.calculate_fare(), expected_fare, places=2)
        
if __name__ == '__main__':
    unittest.main()