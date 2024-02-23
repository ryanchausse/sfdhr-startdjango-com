import os, datetime

from celery import Celery
from celery.schedules import crontab

from form.utilities.APIConnectionUtilities import APIConnectionManager

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'norm.settings')

app = Celery('norm')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Adds token to token buckets every second for outgoing API requests
    # that are regulated by req/s by vendor
    sender.add_periodic_task(1.0, add_tokens_to_buckets.s(), name='addtokenstobuckets')


@app.task
def add_tokens_to_buckets():
    api_mgr = APIConnectionManager()
    if api_mgr.sr_current_requests_per_second_tokens < api_mgr.sr_max_requests_per_second:
        api_mgr.sr_current_requests_per_second_tokens += 1
    if api_mgr.aws_current_requests_per_second_tokens < api_mgr.aws_max_requests_per_second:
        api_mgr.aws_current_requests_per_second_tokens += 1
    print(f'{datetime.datetime.now()} - added one token to bucket '
          'if necessary for SR and AWS')

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
