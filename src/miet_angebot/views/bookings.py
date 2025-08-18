from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.models import Booking
from src.miet_angebot.serializers import (
    ListBookingSerializer,
    RetrieveBookingSerializer,
    CreateUpdateBookingSerializer
)
from src.miet_angebot.permissions import (
    IsAuthor,
    IsListingAuthor,
    CustomActionsPermission,

)
from src.commons.choices import BookingStatusChoice


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        if self.request.user.groups.filter(name="host").exists():
            return self.queryset.select_related("listing").filter(listing__author=self.request.user)
            # return self.queryset.filter(listing__author=self.request.user)
        elif self.request.user.groups.filter(name="guest").exists():
            return self.queryset.filter(author=self.request.user)
        else:
            return self.queryset.none()

    def get_permissions(self):
        if self.action == "list":
            print(self.request.user)
            permissions = [IsAuthenticated(), DjangoModelPermissions()]
        elif self.action in ['create', 'update', 'partial_update']:
            permissions = [IsAuthenticated(), DjangoModelPermissions(), IsAuthor()]
        elif self.action in ['cancel']:
            permissions = [IsAuthenticated(), IsAuthor(), CustomActionsPermission()]
        elif self.action in ['decline', 'accept']:
            permissions = [IsAuthenticated(), IsListingAuthor(), CustomActionsPermission()]
        return permissions

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
              return CreateUpdateBookingSerializer
        elif self.action in ['retrieve']:
            return RetrieveBookingSerializer
        elif self.action in ['list']:
            return ListBookingSerializer
        return ListBookingSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            status=BookingStatusChoice.created.value,)

    @action(url_path="canceled", detail=True, methods=["patch"])
    def cancel(self, request, pk=None):
        try:
            booking = self.get_object()
            serializer = self.get_serializer(
                instance=booking,
                data={'status': BookingStatusChoice.canceled.value},
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Booking cancelled successfully."})
        except Booking.DoesNotExist:
            return Response({"detail": "Booking does not exist."}, 404)
        except Exception as e:
            return Response({"detail": str(e)}, 500)

    @action(url_path="declined", detail=True, methods=["patch"])
    def decline(self, request, pk=None):
        try:
            booking = self.get_object()
            serializer = self.get_serializer(
                instance=booking,
                data={'status': BookingStatusChoice.declined.value},
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Booking declined successfully."})
        except Booking.DoesNotExist:
            return Response({"detail": "Booking does not exist."}, 404)
        except Exception as e:
            return Response({"detail": str(e)}, 500)

    @action(url_path="accepted", detail=True, methods=["patch"])
    def accept(self, request, pk=None):
        try:
            booking = self.get_object()
            serializer = self.get_serializer(
                instance=booking,
                data={'status': BookingStatusChoice.accepted.value},
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Booking accepted successfully."})
        except Booking.DoesNotExist:
            return Response({"detail": "Booking does not exist."}, 404)
        except Exception as e:
            return Response({"detail": str(e)}, 500)
