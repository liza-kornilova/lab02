import unittest
from transport_company import Bus, Route, Client, Ticket, TransportCompany, IDGenerator

class TestTransportCompany(unittest.TestCase):
    def setUp(self):
        IDGenerator._id = 0  # Скидаємо ID перед кожним тестом
        self.company = TransportCompany()
        self.bus = self.company.add_bus("Mercedes Sprinter", 2)
        self.route = self.company.add_route("Kyiv-Lviv", ["Kyiv", "Zhytomyr", "Rivne", "Lviv"], "2024-12-01")
        self.client1 = self.company.add_client("Ivan Petrenko")
        self.client2 = self.company.add_client("Maria Koval")

    def test_bus_creation(self):
        self.assertEqual(self.bus.model, "Mercedes Sprinter")
        self.assertEqual(self.bus.seats, 2)
        self.assertEqual(len(self.bus.available_seats), 2)

    def test_route_creation(self):
        self.assertEqual(self.route.route_name, "Kyiv-Lviv")
        self.assertIn("Kyiv", self.route.stations)
        self.assertIn("Lviv", self.route.stations)
        self.assertEqual(self.route.date, "2024-12-01")

    def test_client_creation(self):
        self.assertEqual(self.client1.name, "Ivan Petrenko")
        self.assertEqual(self.client2.name, "Maria Koval")

    def test_successful_ticket_booking(self):
        ticket = self.company.book_ticket(self.client1, self.bus, self.route, "Kyiv", "Lviv")
        self.assertEqual(ticket.client, self.client1)
        self.assertEqual(ticket.bus, self.bus)
        self.assertEqual(ticket.route, self.route)
        self.assertEqual(ticket.from_station, "Kyiv")
        self.assertEqual(ticket.to_station, "Lviv")

    def test_no_available_seats(self):
        self.company.book_ticket(self.client1, self.bus, self.route, "Kyiv", "Lviv")
        self.company.book_ticket(self.client2, self.bus, self.route, "Kyiv", "Lviv")
        client3 = self.company.add_client("Dmytro Melnyk")
        with self.assertRaises(ValueError) as context:
            self.company.book_ticket(client3, self.bus, self.route, "Kyiv", "Lviv")
        self.assertEqual(str(context.exception), "No available seats in the bus.")

    def test_invalid_station_order(self):
        with self.assertRaises(ValueError) as context:
            self.company.book_ticket(self.client1, self.bus, self.route, "Lviv", "Kyiv")
        self.assertEqual(str(context.exception), "Departure station must precede arrival station.")

if __name__ == '__main__':
    unittest.main()
