from rest_framework.permissions import BasePermission


class IsListingAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.listing.author == request.user