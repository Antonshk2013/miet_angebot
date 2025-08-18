from rest_framework.permissions import BasePermission


class CustomActionsPermission(BasePermission):
    action_permissions_map = {
        'cancel': 'can_cancel_booking',
        'decline': 'can_decline_booking',
        'accept': 'can_accept_booking',
    }

    def has_object_permission(self, request, view, obj):
        if view.action in self.action_permissions_map:
            permission = self.action_permissions_map[view.action]
            perm_name = f"{obj._meta.app_label}.{permission}"
            return request.user.has_perm(perm_name)
        return True