from rest_framework.routers import DefaultRouter

from src.miet_angebot.views import BookingViewSet

router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="bookings")