
from elasticsearch import Elasticsearch
import mandrill
import datetime


def getFromDate():
    return datetime.datetime.now() - datetime.timedelta(minutes=60)

def getClient():
    return  Elasticsearch()

def sent(mailData : dict() ):
    SMTP_PASSWORD = 'arrrtstsfrtr343w4dfrdr2w3'

    mandrill_client = mandrill.Mandrill(SMTP_PASSWORD)

    template_param = buildTemplateParam(mailData)

    email_list = getEmailList()

    message = { 'to': email_list,
        'subject': "Hourly Report",
        'global_merge_vars': template_param,
        'from_email':"saravind506@gmail.com"
    }

    template = "HOURLY_REPORT"

    print(message)
    mandrill_client.messages.send_template(template, [], message)



def buildTemplateParam(mailData):
    template_param = [{"name": "fname",
                       "content": mailData.get("fname")},
                      {"name": "lname",
                       "content": mailData.get("lname")}
                      ]
    return  template_param

def getEmailList():
    email_list = []


    temp_list = dict()
    temp_list['email'] = "mymailbox.aravind@gmail.com"
    temp_list['type'] = 'to'
    email_list.append(temp_list)

    return email_list