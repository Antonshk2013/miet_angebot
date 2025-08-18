from rest_framework.routers import DefaultRouter

from src.miet_angebot.views import ListingViewSet

router = DefaultRouter()
router.register("listings", ListingViewSet, basename="listings")
