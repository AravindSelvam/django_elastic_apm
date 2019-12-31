from django.urls import path
from . import views

urlpatterns = [
path('/sent', views.sent_report, name='sent_report'),
]