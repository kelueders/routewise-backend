import unittest

from kmeans import Itinerary

class TestItinerary(unittest.TestCase):
    # def test_create_dataframe(self):
        # iter = Itinerary(trip_id=391, duration=2)
        # expected = 

    def test_get_duration(self):
        iter = Itinerary(391)
        expected = 4
        self.assertEqual(expected, iter.get_duration)

if __name__ == "__main__":
    unittest.main()
