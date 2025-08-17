from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.filters import ListingFilter
from src.miet_angebot.models import Listing
from src.miet_angebot.serializers import ListingSerializer


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filterset_class = ListingFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price_per_day", "created_at"]



    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name="host").exists():
            return self.queryset.filter(author=self.request.user)
        elif self.request.user.groups.filter(name="guest").exists():
            return self.queryset.filter(is_active=True)
        else:
            return self.queryset.none()


    #TODO
    # def get_serializer_class(self):
    #     ...
