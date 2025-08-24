import logging

from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from src.miet_angebot.filters import ListingFilter
from src.miet_angebot.models import Listing, SearchWords
from src.miet_angebot.models.counter_listing import CounterListing
from src.miet_angebot.permissions import (
    IsAuthor,
    CustomModelPermissions,
    DistrictAll
)
from src.miet_angebot.serializers import (
    GuestListListingSerializer,
    GuestRetrieveListingSerializer,
    HostListingSerializer,
    HostRetrieveListingSerializer,
    ListingSerializer, SearchWordsSerializer,
)

from src.commons.mixins import UserGroupMixin

logger = logging.getLogger(__name__)

class ListingViewSet(UserGroupMixin, ModelViewSet):
    filterset_class = ListingFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["price_per_day", "created_at"]
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        queryset = Listing.objects.all()
        if self.user_group=="host":
            queryset = queryset.filter(author=self.request.user)
        elif self.user_group=="guest":
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.none()
        return queryset

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
        permissions = [
            DistrictAll()
        ]
        if self.user_group == "host":
            if self.action in ["list"]:
                permissions = [IsAuthenticated(), CustomModelPermissions()]
            elif self.action in ['create', 'retrieve', 'update', 'partial_update']:
                permissions = [IsAuthenticated(), CustomModelPermissions(), IsAuthor()]
            elif self.action in ['destroy']:
                permissions = [IsAuthenticated(), CustomModelPermissions(), IsAuthor()]
        if self.user_group == "guest":
            if self.action in ["list", "retrieve"]:
                permissions = [IsAuthenticated(), CustomModelPermissions()]
            if self.action in ['top_search']:
                permissions = [IsAuthenticated()]
        return permissions

    def add_counter(self, instance):
        counter = CounterListing.objects.create(
            listing=instance,
            author=self.request.user,
        )
        counter.save()

    def list(self, request, *args, **kwargs):
        search = request.query_params.get("search")
        logger.info(
            f"[ListingViewSet.list] user={request.user} "
            f"query_params={dict(request.query_params)}"
        )
        if self.user_group == "guest" and search:
            SearchWords.objects.create(
                word=search,
            )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.user_group == "guest":
            self.add_counter(instance)
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def top_search(self, request, *args, **kwargs):
        try:
            results = SearchWords.objects.all()[:10]
            serializer = SearchWordsSerializer(results, many=True)
            return Response({"results": serializer.data}, 200)
        except Exception as e:
            return Response({"detail": str(e)}, 500)

