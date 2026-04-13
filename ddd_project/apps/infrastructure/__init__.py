"""Infrastructure Layer - Persistence and Repository Implementations"""
from django.apps import AppConfig


class InfrastructureConfig(AppConfig):
    name = "ddd_project.apps.infrastructure"
    label = "infrastructure"
    verbose_name = "Infrastructure"


default_app_config = "ddd_project.apps.infrastructure.InfrastructureConfig"