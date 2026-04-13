"""Presentation Layer - API endpoints and handlers"""
from django.apps import AppConfig


class PresentationConfig(AppConfig):
    name = "ddd_project.apps.presentation"
    label = "presentation"
    verbose_name = "Presentation"


default_app_config = "ddd_project.apps.presentation.PresentationConfig"