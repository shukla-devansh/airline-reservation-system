# ✈ SkyWave Airlines — Django Reservation System

A full-featured airline reservation system built with Django.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install django
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Seed sample data (airports, flights, users)
```bash
python manage.py seed_data
```

### 4. Start the server
```bash
python manage.py runserver
```

### 5. Open in browser
```
http://127.0.0.1:8000/
```

---

## 👤 Demo Accounts

| Role  | Username | Password   |
|-------|----------|------------|
| User  | demo     | demo1234   |
| Admin | admin    | admin1234  |

Admin panel: `http://127.0.0.1:8000/admin/`

---

## ✨ Features

- **Flight Search** — Search by origin, destination, date, class, and passengers
- **Multi-class Booking** — Economy, Business, First Class fares
- **Passenger Details** — Full passenger form with DOB and passport
- **Booking Management** — View and cancel reservations
- **Booking Reference** — Unique 8-character alphanumeric reference per booking
- **User Auth** — Register, Login, Logout
- **15 Airports** — Indian domestic + international routes
- **210 Sample Flights** — 2 weeks of scheduled flights
- **Django Admin** — Full model administration

---

## 📁 Project Structure

```
airline_system/
├── airline/                  # Django project config
│   ├── settings.py
│   └── urls.py
├── reservations/             # Main app
│   ├── models.py             # Airport, Flight, Booking, Passenger
│   ├── views.py              # All views
│   ├── urls.py               # URL routing
│   ├── forms.py              # Search, Booking, Auth forms
│   ├── static/css/style.css  # Full CSS design system
│   └── management/commands/
│       └── seed_data.py      # Sample data seeder
├── templates/
│   ├── base.html             # Base layout with navbar
│   └── reservations/
│       ├── home.html         # Landing + search
│       ├── search_results.html
│       ├── flight_detail.html
│       ├── book_flight.html
│       ├── booking_confirmation.html
│       ├── my_bookings.html
│       ├── login.html
│       └── register.html
├── manage.py
└── db.sqlite3                # SQLite database (auto-created)
```

---

## 🎨 Design System

- **Colors:** Deep Navy `#0C1B33`, Sky Blue `#1E90C8`, Amber `#E8A020`
- **Fonts:** Syne (headings) + DM Sans (body) via Google Fonts
- **No gradients** — flat, clean, professional aesthetic
- **Fully responsive** — works on mobile and desktop

---

## 🔧 Models

- **Airport** — IATA code, name, city, country
- **Flight** — Route, times, seats, 3-tier pricing, status
- **Booking** — Reference, user, flight, class, passengers, price
- **Passenger** — Name, DOB, passport per booking

---

## 📝 Sample Routes Available

| Route | Code |
|-------|------|
| Delhi ↔ Mumbai | SW101/102 |
| Delhi → Bangalore | SW201 |
| Delhi → Dubai | SW701 |
| Mumbai → Singapore | SW801 |
| Delhi → London | SW901 |
| + 10 more domestic/international routes | |
