import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','ayim.settings')

app = Celery('ayim')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# для запуска Celery
#python3 -m celery -A <project_name> worker -l info 
#                    <shop_api>