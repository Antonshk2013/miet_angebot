from django.urls import path, include

urlpatterns = [
    path('', include('src.miet_angebot.urls')),
    path('auth/', include('src.users.urls')),
]