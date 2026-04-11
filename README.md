# SkyWave Airlines Reservation System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-settings-092E20.svg?logo=django)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A robust, full-featured airline reservation and management system built with the Django web framework. SkyWave Airlines provides a seamless booking experience for passengers and a comprehensive administration interface for airline staff.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Demo Credentials](#demo-credentials)
- [Project Structure](#project-structure)
- [Design System](#design-system)

## Features

- **Advanced Flight Search**: Query flights by origin, destination, departure date, travel class, and number of passengers.
- **Multi-Tier Pricing**: Support for Economy, Business, and First Class fare structures.
- **Secure User Authentication**: Complete registration, login, and secure session management.
- **Booking Management**: Users can view their itineraries, track booking statuses, and cancel reservations.
- **Automated PNR Generation**: Unique 8-character alphanumeric booking reference assigned per reservation.
- **Comprehensive Admin Dashboard**: Django-powered administration panel for managing airports, routes, and bookings.
- **Pre-configured Dataset**: Includes 15 major airports (domestic and international) and 210 sample scheduled flights.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (Default, configurable to PostgreSQL/MySQL)
- **Frontend:** HTML5, CSS3, Django Templates
- **Styling:** Custom CSS with responsive design principles

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/shukla-devansh/airline-reservation-system.git
   cd airline-reservation-system
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Seed the database with sample data**
   *(Populates airports, flights, and default users)*
   ```bash
   python manage.py seed_data
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your web browser and navigate to `http://127.0.0.1:8000/`

## Demo Credentials

To test the application without registering a new account, you can use the following pre-configured user roles:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Customer** | `demo` | `demo1234` | Standard booking and user dashboard access |
| **Administrator** | `admin` | `admin1234` | Full access including Django Admin panel (`/admin/`) |

## Project Structure

```text
airline_system/
├── airline/                  # Core Django project configuration
│   ├── settings.py
│   └── urls.py
├── reservations/             # Main application module
│   ├── models.py             # Database schemas (Airport, Flight, Booking)
│   ├── views.py              # Application logic and controllers
│   ├── urls.py               # Route definitions
│   ├── forms.py              # Form handling and validation
│   ├── static/css/style.css  # Application stylesheet
│   └── management/commands/
│       └── seed_data.py      # Custom CLI command for data population
├── templates/                # HTML Templates
│   ├── base.html             # Master layout component
│   └── reservations/         # App-specific templates via Django DTL
└── manage.py                 # Django command-line utility
```

## Design System

The application utilizes a custom, modern design system without relying on heavy frontend frameworks:
- **Color Palette:** Deep Navy (`#0C1B33`), Sky Blue (`#1E90C8`), Amber (`#E8A020`)
- **Typography:** Syne (Headings) and DM Sans (Body) via Google Fonts
- **Aesthetic:** Flat, clean, professional interface with full cross-device responsiveness.

##  Models

- **Airport** — IATA code, name, city, country
- **Flight** — Route, times, seats, 3-tier pricing, status
- **Booking** — Reference, user, flight, class, passengers, price
- **Passenger** — Name, DOB, passport per booking

---

##  Sample Routes Available

| Route | Code |
|-------|------|
| Delhi ↔ Mumbai | SW101/102 |
| Delhi → Bangalore | SW201 |
| Delhi → Dubai | SW701 |
| Mumbai → Singapore | SW801 |
| Delhi → London | SW901 |
| ~210 total domestic/international routes | |
