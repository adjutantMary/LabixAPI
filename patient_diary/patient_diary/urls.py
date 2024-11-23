from django.urls import path
from api.endpoints import api

urlpatterns = [
    path("api/", api.urls),
]
