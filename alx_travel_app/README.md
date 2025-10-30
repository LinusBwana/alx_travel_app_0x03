# Property Booking API

A Django REST API for managing property rentals, bookings, and reviews in Kenya - similar to Airbnb, with integrated payment processing via Chapa.

## Features

- **Property Management**: Full CRUD operations for rental properties across Kenya
- **User Bookings**: Complete booking system with date validation and conflict prevention
- **Review System**: Rate and review properties after completed stays
- **Payment Processing**: Integrated Chapa payment gateway for secure transactions
- **Nested Routes**: Access property-specific bookings via nested endpoints
- **Data Seeding**: Generate sample Kenyan property data for testing

## Models

- **Property**: Rental listings with host, location, price in KES, and details
- **Booking**: Reservations with dates, pricing, and status tracking
- **Review**: User reviews with ratings (1-5 stars) and comments
- **Payment**: Payment records linked to bookings with Chapa integration

## Quick Start

```bash
# Clone and setup
git clone <your-repo-url>
cd property-booking-api
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Create sample Kenyan property data
python manage.py populate_db

# Create admin user (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Configuration

### Chapa Payment Setup

Add the following to your `settings.py`:

```python
# Chapa API Configuration
CHAPA_SECRET_KEY = 'your-chapa-secret-key'
CHAPA_API_URL = 'https://api.chapa.co/v1'
PAYMENT_CALLBACK_URL = 'https://yourdomain.com/api/payments/callback/'
```

Set the environment variable:

```bash
export CHAPA_SECRET_KEY='your-actual-secret-key'
```

## Sample Data

The seeder creates realistic Kenyan properties including:
- **Locations**: Nairobi, Mombasa, Maasai Mara, Lake Naivasha, Lamu, etc.
- **Property types**: Beach houses, safari lodges, city apartments, tea estate bungalows
- **Pricing**: KES 3,000 - 25,000 per night
- **Bookings & Reviews**: Realistic booking patterns and guest reviews

## Seeder Options

```bash
# Basic seeding
python manage.py populate_db

# Custom data counts
python manage.py populate_db --users 15 --properties 30 --bookings 50 --reviews 40

# Clear and reseed
python manage.py populate_db --clear
```

## API Endpoints

### Properties

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/properties/` | List all properties |
| POST | `/api/properties/` | Create a new property |
| GET | `/api/properties/{property_id}/` | Retrieve a specific property |
| PUT | `/api/properties/{property_id}/` | Update a property (full) |
| PATCH | `/api/properties/{property_id}/` | Update a property (partial) |
| DELETE | `/api/properties/{property_id}/` | Delete a property |

**Property Response Fields:**
- `property_id` (UUID) - Unique identifier
- `host` (Object) - Host user details
- `name` (String) - Property name
- `description` (Text) - Property description
- `location` (String) - Property location
- `pricepernight` (Decimal) - Price per night in KES
- `average_rating` (Float) - Calculated average rating
- `total_reviews` (Integer) - Count of reviews
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings/` | List all bookings |
| POST | `/api/bookings/` | Create a new booking |
| GET | `/api/bookings/{booking_id}/` | Retrieve a specific booking |
| PUT | `/api/bookings/{booking_id}/` | Update a booking (full) |
| PATCH | `/api/bookings/{booking_id}/` | Update a booking (partial) |
| DELETE | `/api/bookings/{booking_id}/` | Delete a booking |

**Booking Response Fields:**
- `booking_id` (UUID) - Unique identifier
- `property` (Object) - Full property details
- `user` (Object) - User who made the booking
- `start_date` (Date) - Check-in date
- `end_date` (Date) - Check-out date
- `nights` (Integer) - Calculated number of nights
- `total_price` (Decimal) - Total booking price in KES
- `status` (String) - Booking status (pending, confirmed, cancelled, completed)
- `created_at` (DateTime) - Booking creation timestamp

### Nested Booking Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/properties/{property_id}/bookings/` | List all bookings for a specific property |
| POST | `/api/properties/{property_id}/bookings/` | Create a booking for a specific property |
| GET | `/api/properties/{property_id}/bookings/{booking_id}/` | Retrieve a specific booking for a property |
| PUT | `/api/properties/{property_id}/bookings/{booking_id}/` | Update a booking for a property |
| PATCH | `/api/properties/{property_id}/bookings/{booking_id}/` | Partially update a booking for a property |
| DELETE | `/api/properties/{property_id}/bookings/{booking_id}/` | Delete a booking for a property |

### Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/payments/` | List all payments |
| POST | `/api/payments/` | Create a new payment |
| GET | `/api/payments/{payment_id}/` | Retrieve a specific payment |
| PUT | `/api/payments/{payment_id}/` | Update a payment (full) |
| PATCH | `/api/payments/{payment_id}/` | Update a payment (partial) |
| DELETE | `/api/payments/{payment_id}/` | Delete a payment |
| POST | `/api/payments/{payment_id}/initiate/` | Initiate payment via Chapa |

**Payment Response Fields:**
- `id` (Integer) - Payment record ID
- `booking` (UUID) - Associated booking ID
- `amount` (Decimal) - Payment amount in currency
- `payment_status` (String) - Payment status (pending, confirmed, cancelled)
- `transaction_id` (String) - Unique Chapa transaction reference
- `created_at` (DateTime) - Payment creation timestamp
- `updated_at` (DateTime) - Last update timestamp

## API Request Examples

### Create a Property

```bash
POST /api/properties/
Content-Type: application/json

{
  "host_id": 1,
  "name": "Beachfront Villa - Diani",
  "description": "Stunning 3-bedroom villa with ocean views",
  "location": "Diani Beach, Mombasa",
  "pricepernight": 15000
}
```

### Create a Booking

```bash
POST /api/bookings/
Content-Type: application/json

{
  "property_id": "uuid-of-property",
  "user_id": 2,
  "start_date": "2025-11-01",
  "end_date": "2025-11-05",
  "total_price": 60000,
  "status": "pending"
}
```

### Initiate Payment via Chapa

```bash
POST /api/payments/{booking_id}/initiate/
Content-Type: application/json
```

**Response:**
```json
{
  "payment": {
    "id": 1,
    "booking": "uuid-of-booking",
    "amount": "60000.00",
    "payment_status": "pending",
    "transaction_id": "uuid-of-booking",
    "created_at": "2025-10-19T10:30:00Z",
    "updated_at": "2025-10-19T10:30:00Z"
  },
  "payment_url": "https://checkout.chapa.co/..."
}
```

### Update a Property (Partial)

```bash
PATCH /api/properties/{property_id}/
Content-Type: application/json

{
  "pricepernight": 18000,
  "description": "Updated description with new amenities"
}
```

### List Property-Specific Bookings

```bash
GET /api/properties/{property_id}/bookings/
```

## Validation Rules

### Booking Validations
- **Date Range**: End date must be after start date
- **Past Dates**: Start date cannot be in the past
- **Availability**: Property must be available for selected dates (no overlapping confirmed/pending bookings)
- **Price**: Total price must be greater than 0

### Property Validations
- **Price**: Price per night must be greater than 0

### Payment Validations
- **Amount**: Payment amount must be at least 0.01
- **Transaction ID**: Must be unique and cannot be duplicated

## Response Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Payment Flow

1. **Create Booking**: User books a property and creates a booking record
2. **Initiate Payment**: Call the payment initiation endpoint with the booking ID
3. **Redirect to Chapa**: User is redirected to Chapa checkout URL
4. **Payment Processing**: User completes payment on Chapa
5. **Callback**: Chapa sends confirmation callback to your configured endpoint
6. **Update Status**: Payment status is updated based on callback response

## Tech Stack

- Django 4.x
- Django REST Framework
- drf-nested-routers (for nested routes)
- Chapa Payment Gateway
- PostgreSQL/SQLite
- UUID primary keys
- Requests library (for API calls)

## Project Structure

```
property-booking-api/
├── api/
│   ├── models.py          # Property, Booking, Review, Payment models
│   ├── serializers.py     # DRF serializers with validation
│   ├── views.py           # ViewSets for CRUD operations
│   ├── urls.py            # API routing configuration
│   └── management/
│       └── commands/
│           └── populate_db.py
├── manage.py
├── requirements.txt
└── README.md
```