from src.miet_angebot.urls.listings import router as listings_router
from src.miet_angebot.urls.bookings import router as bookings_router

urlpatterns = []

urlpatterns += listings_router.urls
urlpatterns += bookings_router.urls