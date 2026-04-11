from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reservations.models import Airport, Flight
from datetime import datetime, timedelta
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create airports
        airports_data = [
            ('DEL', 'Indira Gandhi International Airport', 'New Delhi', 'India'),
            ('BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'India'),
            ('BLR', 'Kempegowda International Airport', 'Bangalore', 'India'),
            ('MAA', 'Chennai International Airport', 'Chennai', 'India'),
            ('HYD', 'Rajiv Gandhi International Airport', 'Hyderabad', 'India'),
            ('CCU', 'Netaji Subhas Chandra Bose International Airport', 'Kolkata', 'India'),
            ('GOI', 'Goa International Airport', 'Goa', 'India'),
            ('AMD', 'Sardar Vallabhbhai Patel International Airport', 'Ahmedabad', 'India'),
            ('PNQ', 'Pune Airport', 'Pune', 'India'),
            ('COK', 'Cochin International Airport', 'Kochi', 'India'),
            ('DXB', 'Dubai International Airport', 'Dubai', 'UAE'),
            ('SIN', 'Changi Airport', 'Singapore', 'Singapore'),
            ('LHR', 'Heathrow Airport', 'London', 'UK'),
            ('JFK', 'John F. Kennedy International Airport', 'New York', 'USA'),
            ('BKK', 'Suvarnabhumi Airport', 'Bangkok', 'Thailand'),
        ]

        airports = {}
        for code, name, city, country in airports_data:
            airport, _ = Airport.objects.get_or_create(
                code=code,
                defaults={'name': name, 'city': city, 'country': country}
            )
            airports[code] = airport

        self.stdout.write(f'  ✓ Created {len(airports)} airports')

        # Create flights
        routes = [
            ('DEL', 'BOM', 'SW101', 2, 2, 4500, 12000, 28000),
            ('BOM', 'DEL', 'SW102', 2, 2, 4500, 12000, 28000),
            ('DEL', 'BLR', 'SW201', 2, 40, 5200, 14000, 32000),
            ('BLR', 'DEL', 'SW202', 6, 40, 5200, 14000, 32000),
            ('DEL', 'HYD', 'SW301', 7, 0, 4800, 13000, 30000),
            ('BOM', 'GOI', 'SW401', 8, 30, 2800, 8000, 18000),
            ('DEL', 'CCU', 'SW501', 9, 0, 5500, 15000, 35000),
            ('MAA', 'BOM', 'SW601', 10, 30, 4200, 11000, 26000),
            ('DEL', 'DXB', 'SW701', 14, 0, 12000, 35000, 85000),
            ('BOM', 'SIN', 'SW801', 0, 30, 14500, 42000, 98000),
            ('DEL', 'LHR', 'SW901', 22, 0, 35000, 95000, 220000),
            ('BLR', 'DXB', 'SW1001', 6, 0, 11000, 32000, 78000),
            ('HYD', 'BLR', 'SW1101', 11, 0, 2500, 7000, 16000),
            ('DEL', 'AMD', 'SW1201', 13, 0, 3200, 9000, 21000),
            ('BOM', 'COK', 'SW1301', 17, 30, 3800, 10500, 24000),
        ]

        base = timezone.now().replace(minute=0, second=0, microsecond=0)
        flights_created = 0

        for orig_code, dest_code, fn, dep_hour, dep_min, eco, biz, first in routes:
            orig = airports[orig_code]
            dest = airports[dest_code]

            for day_offset in range(0, 14):
                dep = base.replace(hour=dep_hour, minute=dep_min) + timedelta(days=day_offset)
                duration_minutes = random.randint(60, 180) if orig_code not in ('DEL', 'BOM') or dest_code not in ('DXB', 'SIN', 'LHR') else random.randint(300, 600)
                arr = dep + timedelta(minutes=duration_minutes)
                flight_num = f"{fn}-{day_offset+1:02d}"

                if not Flight.objects.filter(flight_number=flight_num).exists():
                    seats = random.choice([120, 150, 180, 220])
                    avail = random.randint(int(seats * 0.3), seats)
                    Flight.objects.create(
                        flight_number=flight_num,
                        origin=orig,
                        destination=dest,
                        departure_time=dep,
                        arrival_time=arr,
                        total_seats=seats,
                        available_seats=avail,
                        economy_price=eco,
                        business_price=biz,
                        first_class_price=first,
                        status='scheduled',
                        airline_name='SkyWave Airlines',
                    )
                    flights_created += 1

        self.stdout.write(f'  ✓ Created {flights_created} flights')

        # Create demo user
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user(
                username='demo', password='demo1234',
                email='demo@skywave.in', first_name='Demo', last_name='User'
            )
            self.stdout.write('  ✓ Demo user: demo / demo1234')

        # Create admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', password='admin1234',
                email='admin@skywave.in'
            )
            self.stdout.write('  ✓ Admin user: admin / admin1234')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
