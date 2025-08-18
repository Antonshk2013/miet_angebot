from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.filters import ListingFilter
from src.miet_angebot.models import Listing
from src.miet_angebot.permissions import (
    IsAuthor,
    CustomModelPermissions,
)
from src.miet_angebot.serializers import (
    GuestListListingSerializer,
    GuestRetrieveListingSerializer,
    HostListingSerializer,
    HostRetrieveListingSerializer,
    ListingSerializer,
)


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    filterset_class = ListingFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price_per_day", "created_at"]
    http_method_names = ["get", "post", "patch", "put", "delete"]
    user_group = None


    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.groups.filter(name="host").exists():
            self.user_group = "host"
        elif request.user.groups.filter(name="guest").exists():
            self.user_group = "guest"
        else:
            self.user_group = None

    def get_queryset(self):
        if self.user_group=="host":
            print(self.request.build_absolute_uri())
            return self.queryset.filter(author=self.request.user)
        elif self.user_group=="guest":
            return self.queryset.filter(is_active=True)
        else:
            return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        serializer_class = ListingSerializer
        if self.user_group=="host":
            if self.action == "list":
                serializer_class = HostListingSerializer
                return serializer_class
            if self.action == "retrieve":
                serializer_class = HostRetrieveListingSerializer
                return serializer_class
        if self.user_group=="guest":
            if self.action == "list":
                serializer_class = GuestListListingSerializer
                return GuestListListingSerializer
            if self.action == "retrieve":
                serializer_class = GuestRetrieveListingSerializer
                return GuestRetrieveListingSerializer
        return serializer_class

    def get_permissions(self):
        if self.action in ["list"]:
            permissions = [IsAuthenticated(), CustomModelPermissions()]
        elif self.action in ['create', 'retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated(), CustomModelPermissions(), IsAuthor()]
        elif self.action in ['destroy']:
            permissions = [IsAuthenticated(), CustomModelPermissions(), IsAuthor()]
        else:
            permissions = [IsAuthenticated(), CustomModelPermissions()]
        return permissions

