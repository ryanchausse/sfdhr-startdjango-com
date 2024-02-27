# Celery tasks (async functions, basically)
from celery import Celery
from celery import shared_task
from django.core.mail import EmailMessage
from .models import EligibleList
from .utilities.APIConnectionUtilities import APIConnectionManager
from django.conf import settings
from celery.utils.log import get_task_logger
import os, datetime

@shared_task
def add_tokens_to_buckets():
    # To run every second - implements Token Bucket algorithm
    # This may tax RabbitMQ/Celery/DB and be better replaced by a
    # "while True" loop
    logger = get_task_logger(name='add_token_logger')
    api_conn_mgr = APIConnectionManager()
    api_conn_mgr.sr_add_token_for_requests_per_second()
    logger.info(f'{datetime.datetime.now()} - added one token to bucket for SR')
    api_conn_mgr.aws_add_token_for_requests_per_second()
    logger.info(f'{datetime.datetime.now()} - added one token to bucket for AWS')
    return (f'Current SR request per second tokens: {api_conn_mgr.sr_get_current_requests_per_second_tokens()}. '
            f'Current AWS request per second tokens: {api_conn_mgr.aws_get_current_requests_per_second_tokens()}.')

@shared_task
def email_score_report_or_el(el_id, report_type='score_report'):
    el_object = EligibleList.objects.get(pk=el_id)
    if report_type == 'score_report':
        email_subject = f'New Score Report: {el_object.code}'
        email_message_body = (f'Hello EIS Team!\n\n'
                         f'There is a new Score Report to post on the SFDHR website.\n\n'
                         f'Please see the attached file.')
        uri = f"/pdfs/score_reports/score_report_{el_object.code}.pdf"
        email = EmailMessage(
            email_subject,
            email_message_body,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_TO,],
        )
        email.attach_file(os.path.abspath(os.path.dirname(__file__)) + uri)
        # Do we need to return something?
        return email.send(fail_silently=False)
    elif report_type == 'eligible_list':
        email_subject = f'New Eligible List: {el_object.code}'
        email_message_body = (f'Hello EIS Team!\n\n'
                         f'There is a new Eligible List to post on the SFDHR website.\n\n'
                         f'Please see the attached file.')
        uri = f"/pdfs/eligible_lists/eligible_list_{el_object.code}.pdf"
        email = EmailMessage(
            email_subject,
            email_message_body,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_TO,],
        )
        email.attach_file(os.path.abspath(os.path.dirname(__file__)) + uri)
        # Do we need to return something?
        return email.send(fail_silently=False)
    return False