from django.urls import path
from ddd_project.apps.presentation.api import api

urlpatterns = [
    path("api/", api.urls),
]