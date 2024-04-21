from database import *
import unittest
class TestDatabase(unittest.TestCase):
    def test_Performance_Tracker(self):
        remove_elements('Performance')
        x = performance_stat_tracker('Chad', 1000, 1000)
        self.assertEqual(x, 1)
        performance_stat_tracker('Chad', 100, 100, start=False, game_id=x, hands_played=100)
        y = performance_stat_tracker('Chad2', 500, 5000)
        self.assertEqual(y, 2)
        performance_stat_tracker('Chad2', 100, 100, start=False, game_id=y, hands_played=100)




if __name__ == '__main__':
    unittest.main()
