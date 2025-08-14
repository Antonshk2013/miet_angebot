from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.models import Booking
from src.miet_angebot.serializers import BookingSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ["get", "post", "put", "patch"]

    # `create()`
    # `retrieve()`
    # `update()`
    # `partial_update()`
    # `destroy()`
    # `list()`

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #TODO
    # def get_queryset(self):
    #     user = self.request.user
    #     ...

    #TODO
    # def get_permissions(self):
    #     ...



