from django.apps import AppConfig  # ✅ THIS LINE IS MISSING IN YOUR FILE

class LmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms'

    # Remove this if you’re not using signals.py
    # def ready(self):
    #     import lms.signals