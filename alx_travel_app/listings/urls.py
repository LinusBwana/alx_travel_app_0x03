from django.urls import include, path
from .views import PropertyViewSet, BookingViewSet, PaymentViewSet
from rest_framework_nested import routers

# main/global routes
router = routers.DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'payments', PaymentViewSet, basename='payments')

# nested routes: bookings under properties
properties_router = routers.NestedDefaultRouter(router, r'properties', lookup='property')
properties_router.register(r'bookings', BookingViewSet, basename='property-bookings')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(properties_router.urls)),
]