from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.miet_angebot.models import Listing
from src.miet_angebot.serializers import ListingSerializer


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    # permission_classes = [IsAuthenticated]
    # http_method_names = ["get", "post", "put", "patch", "delete"]
    #list, create, retrive + action Canseled + action Confirm
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    #TODO
    # def get_queryset(self):
    #     ...

    #TODO
    # def get_serializer_class(self):
    #     ...
