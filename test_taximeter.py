# ¿Qué hacen estos tests?
# Comprueban que el cálculo de tarifas sea correcto en diferentes escenarios
# Verifican que el tiempo se acumule adecuadamente según el estado.
# Usan time.sleep() para simular el paso del tiempo
# Ejecución:
# python3 -m unittest test_taximeter.py


import unittest
import time
from taximetro_medio import calculate_fare, update_state_time

class TestTaximeterFunctions(unittest.TestCase):
    
    def test_calculate_fare_zero(self):
        self.assertEqual(calculate_fare(0, 0), 0.0)
        
    def test_calculate_fare_only_stopped(self):
        self.assertEqual(calculate_fare(10, 0), 0.2)
        
    def test_calculate_fare_only_moving(self):
        self.assertEqual(calculate_fare(0, 10), 0.5)
        
    def test_calculate_fare_combined(self):
        self.assertAlmostEqual(calculate_fare(5, 5), 0.35)
        
    def test_update_state_time_stopped(self):
        stopped_time = 0
        moving_time = 0
        state = 'stopped'
        start = time.perf_counter()
        time.sleep(0.1) # Simular espera
        new_stopped, new_moving  = update_state_time(state, start, stopped_time, moving_time)
        self.assertGreater(new_stopped, 0.09)
        self.assertEqual(new_moving, 0)
        
    def test_update_state_time_moving(self):
        stopped_time = 0
        moving_time = 0
        state = 'moving'
        start = time.perf_counter()
        time.sleep(0.1) # Simular espera
        new_stopped, new_moving = update_state_time(state, start, stopped_time, moving_time)
        self.assertEqual(new_stopped, 0)
        self.assertGreater(new_moving, 0.09)
        
if __name__ == '__main__':
    unittest.main()
        
        