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
    CustomActionsPermission, DistrictAll,

)
from src.commons.choices import BookingStatusChoice


class BookingViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch"]
    user_group = None

    def initial(self, request, *args, **kwargs):
        if request.user.groups.filter(name="host").exists():
            self.user_group = "host"
        elif request.user.groups.filter(name="guest").exists():
            self.user_group = "guest"
        else:
            self.user_group = None
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Booking.objects.all()
        if self.user_group=="host":
            queryset = queryset.select_related("listing").filter(listing__author=self.request.user)
        elif self.user_group=="guest":
            queryset = queryset.filter(author=self.request.user)
        else:
            queryset = queryset.none()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            status=BookingStatusChoice.created.value,)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
              return CreateUpdateBookingSerializer
        elif self.action in ['retrieve']:
            return RetrieveBookingSerializer
        elif self.action in ['list']:
            return ListBookingSerializer
        return ListBookingSerializer


    def get_permissions(self):
        permissions = [
            DistrictAll()
        ]
        if self.action == "list":
            permissions = [IsAuthenticated(), DjangoModelPermissions()]
        elif self.action in ['create', 'update', 'partial_update']:
            permissions = [IsAuthenticated(), DjangoModelPermissions(), IsAuthor()]
        elif self.action in ['cancel']:
            permissions = [IsAuthenticated(), IsAuthor(), CustomActionsPermission()]
        elif self.action in ['decline', 'accept']:
            permissions = [IsAuthenticated(), IsListingAuthor(), CustomActionsPermission()]
        return permissions




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
