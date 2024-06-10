from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'
    #label = 'apps_auth'

    def ready(self):
        import apps.authentication.signals