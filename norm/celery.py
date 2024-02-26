import os, datetime

from celery import Celery
from form.utilities.APIConnectionUtilities import APIConnectionManager
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

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

@app.task(bind=True, name='add_tokens_to_buckets')
def add_tokens_to_buckets():
    # To run every second - implements Token Bucket algorithm
    # This may tax RabbitMQ/Celery and be better replaced by a while True loop
    api_mgr = APIConnectionManager()
    if api_mgr.sr_current_requests_per_second_tokens < api_mgr.sr_max_requests_per_second:
        api_mgr.sr_current_requests_per_second_tokens += 1
        logger.info(f'{datetime.datetime.now()} - added one token to bucket for SR')
    if api_mgr.aws_current_requests_per_second_tokens < api_mgr.aws_max_requests_per_second:
        api_mgr.aws_current_requests_per_second_tokens += 1
        logger.info(f'{datetime.datetime.now()} - added one token to bucket for AWS')
    return True

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
