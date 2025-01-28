from django.apps import AppConfig
import logging

class MerchantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'merchant'

    def ready(self):
        # Import and start the scheduler inside the ready method
        from .scheduler import start_scheduler  # Import inside this method to avoid premature loading
        start_scheduler()
        logging.info("Scheduler initialized from apps.py.")