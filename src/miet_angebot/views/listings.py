from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.filters import ListingFilter
from src.miet_angebot.models import Listing
from src.miet_angebot.serializers import (
    GuestListListingSerializer,
    GuestRetrieveListingSerializer,
    HostListingSerializer,
    HostRetrieveListingSerializer,
    ListingSerializer,
)


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filterset_class = ListingFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price_per_day", "created_at"]
    permission_classes = [IsAuthenticated]
    user_group = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.groups.filter(name="host").exists():
            self.user_group = "host"
        elif request.user.groups.filter(name="guest").exists():
            self.user_group = "guest"
        else:
            self.user_group = None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.user_group=="host":
            return self.queryset.filter(author=self.request.user)
        elif self.user_group=="guest":
            return self.queryset.filter(is_active=True)
        else:
            return self.queryset.none()

    def get_serializer_class(self):
        if self.user_group=="host":
            if self.action == "list":
                return HostListingSerializer
            if self.action == "retrieve":
                return HostRetrieveListingSerializer
        if self.user_group=="guest":
            if self.action == "list":
                return GuestListListingSerializer
            if self.action == "retrieve":
                return GuestRetrieveListingSerializer
        return ListingSerializer
