from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Property, Booking, Payment
from .serializers import PropertySerializer, BookingSerializer, PaymentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from django.conf import settings

# Create your views here.
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        property_pk = self.kwargs.get('property_pk') # from NestedDefaultRouter
        if property_pk:
            queryset = queryset.filter(property__property_id=property_pk)
        return queryset
    
class PaymentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling payments via Chapa API.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=True, methods=['POST', 'GET'], url_path='initiate')
    def initiate_payment(self, request, pk=None):
        """
        Initiates a payment for a given booking (pk=booking_id)
        """
        try:
            booking = Booking.objects.get(booking_id=pk)

            payload = {
                "amount": str(booking.total_price),
                "currency": "ETB",  # adjust currency if needed
                "tx_ref": str(booking.booking_id),
                "callback_url": "https://yourdomain.com/payment/callback/",  # replace
                "customer_name": booking.user.username,
                "customer_email": booking.user.email,
            }

            headers = {
                "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                "https://api.chapa.co/v1/transaction/initialize",
                json=payload,
                headers=headers
            )

            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                payment, created = Payment.objects.get_or_create(
                    booking=booking,
                    defaults={
                        "amount": booking.total_price,
                        "payment_status": "pending",
                        "transaction_id": data["data"]["tx_ref"]
                    }
                )

                serializer = PaymentSerializer(payment)
                return Response({
                    "payment": serializer.data,
                    "payment_url": data["data"]["checkout_url"]
                }, status=status.HTTP_201_CREATED)

            return Response({
                "error": data.get("message", "Failed to initiate payment")
            }, status=status.HTTP_400_BAD_REQUEST)

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)