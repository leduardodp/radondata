import os
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect 
from django.template import loader
from django.urls import reverse
from apps.aulas.models import Aula
from django.conf import settings
from django.views.static import serve
from . import tasks
import json



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    # Obtén los grupos del usuario
    user_groups = request.user.groups.all()

    # Filtra las aulas según los grupos del usuario
    aulas = Aula.objects.filter(grupo__in=user_groups).distinct()
    # Añadir medias y concentraciones al contexto
    aulas_info = []
    for aula in aulas:
        aula_info = {
            'nombre': aula.nombre,
            'media_diaria': tasks.get_media_diaria(aula.nombre),
            'media_semanal': tasks.get_media_semanal(aula.nombre),
            'media_mensual': tasks.get_media_mensual(aula.nombre),
            'json': json.dumps(tasks.get_json(aula.nombre)),
        }
        aulas_info.append(aula_info)
    
    context['aulas_info'] = aulas_info

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def error_404_view(request, exception):
    context = {}
    html_template = loader.get_template('home/page-404.html')
    return HttpResponse(html_template.render(context, request))

def error_500_view(request):
    context = {}
    html_template = loader.get_template('home/page-500.html')
    return HttpResponse(html_template.render(context, request),status=500)