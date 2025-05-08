import os
from celery import Celery

# celery -A hostmanager worker -l info

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostmanager.settings')

app = Celery('hostmanager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    'change-root-password-every-8-hours': {
        'task': 'app.tasks.schedule_password_changes',
        'schedule': crontab(minute=0, hour='*/8'),
    },
    'stat-host-count-every-day': {
        'task': 'apps.tasks.stat_host_count',
        'schedule': crontab(minute=0, hour=0),
    },
}
