import os
from celery import Celery

#  Set default django settings module for the "Celery" program

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings"
)
app = Celery("accounts")

app.config_from_object("django.conf.settings", namespace="CELERY")
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()