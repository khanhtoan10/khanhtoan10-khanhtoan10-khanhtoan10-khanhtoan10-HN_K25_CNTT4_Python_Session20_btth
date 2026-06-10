import unittest
from main import calculate_revenue


class TestTicketing(unittest.TestCase):
    def test_mixed_tickets(self):
        tickets = [
            {"price": 100.0, "status": "Booked"},
            {"price": 200.0, "status": "Cancelled"},
            {"price": 300.0, "status": "Booked"}
        ]
        self.assertEqual(calculate_revenue(tickets), 400.0)

    def test_empty_list(self):
        self.assertEqual(calculate_revenue([]), 0.0)


if __name__ == '__main__':
    unittest.main()
