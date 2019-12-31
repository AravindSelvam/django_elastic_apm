import os
from celery import Celery
from celery.task.schedules import crontab

from .utils import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_monitoring.settings')
app = Celery('report')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app.conf.beat_schedule = {
        "sent-report-task": {
            "task": "django_elastic_apm.celery.hourly_report",
            "schedule": crontab(hour="*", minute=1)
        }

    }


@app.task
def hourly_report():
    client = getClient()
    fromTime = getFromDate()
    logger.info("From Date --->" + str(fromTime))
    toTime = datetime.datetime.now()
    logger.info("toTime --->" + str(toTime))

    response = client.search(
        index="user-report-v2",
        body={
            "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "gender": {
              "query": "male"
            }
          }
        },

          {
              "range": {
                  "age": {
                      "gte": 18,
                      "lte": 50
                  }
              }
          },

        {
          "range": {
            "created": {
              "gte": fromTime,
              "lte": toTime
            }
          }
        }
      ]
    }
  }
                }
            )

    print(response)

    if response['hits'] and response['hits']['hits']:
        count = response['hits']['total']['value']
        logger.info("count =>" + str(count))
        sent(response)
    else :
        logger.info("no data available")
