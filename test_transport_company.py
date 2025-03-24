from transport_company import Bus, Route, Client, Ticket, TransportCompany, IDGenerator

# Ініціалізація тестових даних
IDGenerator._id = 0  # Скидаємо ID перед кожним тестом
company = TransportCompany()
bus = company.add_bus("Mercedes Sprinter", 2)  # Маленький автобус для тесту
route = company.add_route("Kyiv-Lviv", ["Kyiv", "Zhytomyr", "Rivne", "Lviv"], "2024-12-01")
client1 = company.add_client("Ivan Petrenko")
client2 = company.add_client("Maria Koval")

# Перевірка створення автобуса
assert bus.model == "Mercedes Sprinter"
assert bus.seats == 2
assert len(bus.available_seats) == 2

# Перевірка створення маршруту
assert route.route_name == "Kyiv-Lviv"
assert "Kyiv" in route.stations
assert "Lviv" in route.stations
assert route.date == "2024-12-01"

# Перевірка створення клієнта
assert client1.name == "Ivan Petrenko"
assert client2.name == "Maria Koval"

# Перевірка успішного бронювання квитка
ticket = company.book_ticket(client1, bus, route, "Kyiv", "Lviv")
assert ticket.client == client1
assert ticket.bus == bus
assert ticket.route == route
assert ticket.from_station == "Kyiv"
assert ticket.to_station == "Lviv"

# Перевірка, що неможливо забронювати більше місць, ніж доступно
company.book_ticket(client2, bus, route, "Kyiv", "Lviv")
try:
    client3 = company.add_client("Dmytro Melnyk")
    company.book_ticket(client3, bus, route, "Kyiv", "Lviv")
except ValueError as e:
    assert str(e) == "No available seats in the bus."

# Перевірка, що станція відправлення не може бути після прибуття
try:
    company.book_ticket(client1, bus, route, "Lviv", "Kyiv")
except ValueError as e:
    assert str(e) == "Departure station must precede arrival station."

print("Усі перевірки пройдено успішно.")
