from rest_framework import serializers
from .models import Property, Booking, Payment
from django.contrib.auth.models import User
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class PropertySerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'property_id', 'host', 'host_id', 'name', 'description', 
            'location', 'pricepernight', 'average_rating', 
            'total_reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = ['property_id', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        """Calculate average rating for the property using related_name 'reviews'"""
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return None

    def get_total_reviews(self, obj):
        """Get total number of reviews using related_name 'reviews'"""
        return obj.reviews.count()

    def validate_price_per_night(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0")
        return value


class BookingSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    property_id = serializers.UUIDField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    nights = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'property', 'property_id', 'user', 'user_id',
            'start_date', 'end_date', 'nights', 'total_price', 
            'status', 'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']

    def get_nights(self, obj):
        """Calculate number of nights"""
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return 0

    def validate(self, data):
        """Custom validation for booking dates and availability"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        property_data = data.get('property')
        user_data = data.get('user')
        
        # Validate date range
        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError(
                    "End date must be after start date"
                )
            
            if start_date < date.today():
                raise serializers.ValidationError(
                    "Start date cannot be in the past"
                )
            
        if property_data and start_date and end_date:
            try:
                property_instance = Property.objects.get(pk=property_data)
                overlapping_bookings = property_instance.bookings.filter(
                    status__in=['pending', 'confirmed'],
                    start_date__lt=end_date,
                    end_date__gt=start_date
                )
                
                # Exclude current booking if updating
                if self.instance:
                    overlapping_bookings = overlapping_bookings.exclude(
                        booking_id=self.instance.booking_id
                    )
                
                if overlapping_bookings.exists():
                    raise serializers.ValidationError(
                        "Property is not available for the selected dates"
                    )
            except Property.DoesNotExist:
                raise serializers.ValidationError("Property does not exist")

        return data

    def validate_total_price(self, total_price):
        if total_price <= 0:
            raise serializers.ValidationError("Total price must be greater than 0")
        return total_price
    

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_status', 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['transaction_id', 'created_at', 'updated_at']
