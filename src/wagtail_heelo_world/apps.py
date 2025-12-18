from django.apps import AppConfig


class WagtailHeeloWorldConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wagtail_heelo_world"
    label = "wagtail_heelo_world"
    verbose_name = "Wagtail Heelo World"

    def ready(self):
        pass  # Import signals here if needed
