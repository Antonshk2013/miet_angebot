class UserGroupMixin:
    user_group = None

    def initial(self, request, *args, **kwargs):
        if request.user.groups.filter(name="host").exists():
            self.user_group = "host"
        elif request.user.groups.filter(name="guest").exists():
            self.user_group = "guest"
        else:
            self.user_group = None
        return super().initial(request, *args, **kwargs)