from django.contrib import admin
from django.urls import path, include
from ddd_project.apps.presentation.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]