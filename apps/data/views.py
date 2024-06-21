# views.py
from  django.shortcuts import HttpResponse
from .tasks import test_func ,send_mail_func

def test(request):
    test_func.delay()
    return HttpResponse("Esta mierda funciona")

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Esta mierda envía correos")





