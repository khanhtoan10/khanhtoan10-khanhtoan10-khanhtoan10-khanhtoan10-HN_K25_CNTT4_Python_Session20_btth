from main import calculate_revenue


def test_mixed_tickets():
    tickets = [
        {"price": 100.0, "status": "Booked"},
        {"price": 200.0, "status": "Cancelled"},
        {"price": 300.0, "status": "Booked"}
    ]
    assert calculate_revenue(tickets) == 400.0


def test_empty_list():
    assert calculate_revenue([]) == 0.0
