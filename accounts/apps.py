from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self, *args, **kwargs) -> None:
        import accounts.signals
        super_ready = super().ready(*args, **kwargs)
        return super_ready
