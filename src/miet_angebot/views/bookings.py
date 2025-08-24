from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.models import Booking
from src.miet_angebot.serializers import (
    ListBookingSerializer,
    RetrieveBookingSerializer,
    CreateUpdateBookingSerializer, CreateCommentSerializer
)
from src.miet_angebot.permissions import (
    IsAuthor,
    IsListingAuthor,
    CustomActionsPermission, DistrictAll, CustomModelPermissions,

)
from src.commons.choices import BookingStatusChoice
from src.commons.mixins import UserGroupMixin


class BookingViewSet(UserGroupMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch"]

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
        elif self.action in ['add_comment']:
            return CreateCommentSerializer


    def get_permissions(self):
        permissions = [
            DistrictAll()
        ]
        if self.action in ["list", "retrieve"]:
            permissions = [IsAuthenticated(), CustomModelPermissions()]
        elif self.action in ['create', 'update', 'partial_update']:
            permissions = [IsAuthenticated(), CustomModelPermissions(), IsAuthor()]
        elif self.action in ['cancel']:
            permissions = [IsAuthenticated(), IsAuthor(), CustomActionsPermission()]
        elif self.action in ['decline', 'accept']:
            permissions = [IsAuthenticated(), IsListingAuthor(), CustomActionsPermission()]
        elif self.action in ['add_comment']:
            permissions = [IsAuthenticated(), IsAuthor(), CustomModelPermissions()]
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

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        try:
            booking = self.get_object()
            context = {**self.get_serializer_context(), "booking": booking}
            serializer = self.get_serializer(
                data=request.data,
                context=context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                    author=self.request.user,
                    booking=booking,
                    listing=booking.listing,
                )
            return Response({"detail": "Comment add successfully."})
        except ValidationError as e:
            return Response({"detail": e.detail}, 400)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking does not exist."}, 404)
        except Exception as e:
            return Response({"detail": str(e)}, 500)
