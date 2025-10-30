# listings/management/commands/populate_db.py
import random
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Property, Booking, Review


class Command(BaseCommand):
    help = 'Populate the database with sample listings data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--properties',
            type=int,
            default=20,
            help='Number of properties to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=25,
            help='Number of reviews to create (default: 25)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Property.objects.all().delete()
            # Don't delete all users as some might be admin users
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.WARNING('Existing data cleared.'))

        # Create users
        self.stdout.write('Creating users...')
        users = self.create_users(options['users'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(users)} users.')
        )

        # Create properties
        self.stdout.write('Creating properties...')
        properties = self.create_properties(users, options['properties'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(properties)} properties.')
        )

        # Create bookings
        self.stdout.write('Creating bookings...')
        bookings = self.create_bookings(users, properties, options['bookings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(bookings)} bookings.')
        )

        # Create reviews
        self.stdout.write('Creating reviews...')
        reviews = self.create_reviews(users, properties, bookings, options['reviews'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(reviews)} reviews.')
        )

        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )

    def create_users(self, count):
        """Create sample users"""
        users = []
        user_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_johnson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Johnson'},
            {'username': 'sarah_wilson', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Wilson'},
            {'username': 'david_brown', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Brown'},
            {'username': 'lisa_davis', 'email': 'lisa@example.com', 'first_name': 'Lisa', 'last_name': 'Davis'},
            {'username': 'tom_miller', 'email': 'tom@example.com', 'first_name': 'Tom', 'last_name': 'Miller'},
            {'username': 'emma_garcia', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Garcia'},
            {'username': 'chris_martinez', 'email': 'chris@example.com', 'first_name': 'Chris', 'last_name': 'Martinez'},
            {'username': 'amy_rodriguez', 'email': 'amy@example.com', 'first_name': 'Amy', 'last_name': 'Rodriguez'},
        ]

        for i in range(count):
            if i < len(user_data):
                data = user_data[i]
            else:
                data = {
                    'username': f'user_{i+1}',
                    'email': f'user{i+1}@example.com',
                    'first_name': f'User',
                    'last_name': f'{i+1}'
                }
            
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            )    
            if created:
                user.set_password('password123')  # Default password for all users
                user.save()
            users.append(user)

        return users

    def create_properties(self, users, count):
        """Create sample properties"""
        property_data = [
            {
                'name': 'Cozy Beach House',
                'description': 'Beautiful oceanfront property with stunning sunset views. Perfect for a romantic getaway or family vacation.',
                'location': 'Diani Beach, Mombasa',
                'pricepernight': Decimal('15000.00')
            },
            {
                'name': 'Downtown Apartment',
                'description': 'Modern apartment in the heart of the city. Walking distance to restaurants, shops, and entertainment.',
                'location': 'Westlands, Nairobi',
                'pricepernight': Decimal('8000.00')
            },
            {
                'name': 'Mountain View Cottage',
                'description': 'Rustic cottage with stunning mountain views. Great for hiking and outdoor activities.',
                'location': 'Nanyuki, Mount Kenya',
                'pricepernight': Decimal('12000.00')
            },
            {
                'name': 'Luxury Safari Lodge',
                'description': 'Spacious lodge with private deck and wildlife views. Perfect for safari experiences.',
                'location': 'Maasai Mara, Narok',
                'pricepernight': Decimal('25000.00')
            },
            {
                'name': 'Historic Stone House',
                'description': 'Charming historic home in the old town. Beautifully restored with modern amenities.',
                'location': 'Stone Town, Lamu',
                'pricepernight': Decimal('10000.00')
            },
            {
                'name': 'Lakefront Cottage',
                'description': 'Peaceful cottage right on the lake with private dock. Perfect for fishing and water activities.',
                'location': 'Lake Naivasha, Nakuru',
                'pricepernight': Decimal('9000.00')
            },
            {
                'name': 'Highland Retreat',
                'description': 'Unique highland property with stunning landscape views. Very private and serene.',
                'location': 'Nyeri, Central Kenya',
                'pricepernight': Decimal('14000.00')
            },
            {
                'name': 'City Studio',
                'description': 'Compact but efficient studio apartment in trendy neighborhood. Perfect for solo travelers.',
                'location': 'Kilimani, Nairobi',
                'pricepernight': Decimal('5000.00')
            },
            {
                'name': 'Tea Estate Bungalow',
                'description': 'Historic bungalow on working tea estate. Experience rural life with beautiful green views.',
                'location': 'Kericho, Rift Valley',
                'pricepernight': Decimal('11000.00')
            },
            {
                'name': 'Coastal Villa',
                'description': 'Luxury villa with ocean views and private beach access. High-end finishes and premium amenities.',
                'location': 'Malindi, Kilifi',
                'pricepernight': Decimal('20000.00')
            }
        ]

        properties = []
        for i in range(count):
            if i < len(property_data):
                data = property_data[i]
            else:
                data = {
                    'name': f'Property {i+1}',
                    'description': f'This is a sample property description for property {i+1}. It offers great amenities and comfort.',
                    'location': random.choice([
                        'Karen, Nairobi', 
                        'Nyali, Mombasa', 
                        'Kisumu, Nyanza', 
                        'Nakuru, Rift Valley', 
                        'Eldoret, Uasin Gishu',
                        'Thika, Kiambu',
                        'Machakos, Eastern',
                        'Kitale, Trans Nzoia'
                    ]),
                    'pricepernight': Decimal(str(random.randint(3000, 20000)))
                }

            property_obj = Property.objects.create(
                host=random.choice(users),
                name=data['name'],
                description=data['description'],
                location=data['location'],
                pricepernight=data['pricepernight']
            )
            properties.append(property_obj)

        return properties

    def create_bookings(self, users, properties, count):
        """Create sample bookings"""
        bookings = []
        booking_statuses = ['pending', 'confirmed', 'canceled']
        
        for i in range(count):
            # Generate random dates
            start_date = date.today() + timedelta(
                days=random.randint(-30, 60)  # Bookings from 30 days ago to 60 days in future
            )
            nights = random.randint(1, 14)  # 1 to 14 nights
            end_date = start_date + timedelta(days=nights)
            
            property_obj = random.choice(properties)
            guest_user = random.choice([u for u in users if u != property_obj.host])
            
            # Check for overlapping bookings
            overlapping = Booking.objects.filter(
                property=property_obj,
                status__in=['pending', 'confirmed'],
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            if overlapping.exists():
                # Skip this booking to avoid conflicts
                continue
            
            total_price = property_obj.pricepernight * nights
            status = random.choice(booking_statuses)
            
            booking = Booking.objects.create(
                property=property_obj,
                user=guest_user,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=status
            )
            bookings.append(booking)

        return bookings

    def create_reviews(self, users, properties, bookings, count):
        """Create sample reviews"""
        reviews = []
        review_comments = [
            "Amazing stay! The property was exactly as described and the host was very responsive.",
            "Great location and beautiful views. Would definitely book again.",
            "Clean and comfortable. Perfect for our weekend getaway.",
            "The property exceeded our expectations. Highly recommended!",
            "Good value for money. Nice amenities and peaceful environment.",
            "Lovely place with great attention to detail. Host was very welcoming.",
            "Perfect location for exploring the area. Very convenient.",
            "Beautiful property with stunning views. Great for relaxation.",
            "Clean, comfortable, and well-equipped. Everything we needed was provided.",
            "Wonderful experience! The property photos don't do it justice.",
            "Great communication from the host. Check-in was seamless.",
            "Perfect for a romantic getaway. Very private and peaceful.",
            "Family-friendly property with lots of space. Kids loved it!",
            "Good location but could use some updates to the furniture.",
            "Nice property overall. A few minor issues but nothing major."
        ]

        # Only create reviews for completed bookings
        completed_bookings = [
            b for b in bookings 
            if b.status == 'confirmed' and b.end_date < date.today()
        ]

        review_count = 0
        for booking in completed_bookings:
            if review_count >= count:
                break
                
            # Only create review if one doesn't already exist
            existing_review = Review.objects.filter(
                property=booking.property,
                user=booking.user
            ).first()
            
            if not existing_review:
                review = Review.objects.create(
                    property=booking.property,
                    user=booking.user,
                    rating=random.randint(3, 5),  # Mostly positive reviews
                    comment=random.choice(review_comments)
                )
                reviews.append(review)
                review_count += 1

        return reviews