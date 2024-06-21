# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('sendmail', views.send_mail_to_all, name='sendmail'),
]
