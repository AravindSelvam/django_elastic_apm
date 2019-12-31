import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django_elastic_apm.celery import hourly_report

def sent_report(request,**kwargs):
    hourly_report.delay()
    logger.info("mail alert triggerd")
    return HttpResponse("mail triggerd successfully")