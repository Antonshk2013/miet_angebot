from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.models import Listing
from src.miet_angebot.serializers import ListingSerializer


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
