from django.urls import path, include

urlpatterns = [
    path('', include('src.miet_angebot.urls')),
    path('custom_auth/', include('src.users.urls')),
]