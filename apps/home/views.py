import os
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.data import read_data
from django.conf import settings
from django.views.static import serve


read_data.async_task()

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    context['concentracion'] = read_data.concentracion_funcion()
    context['media'] = read_data.media_funcion()

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        #Verifica si la ruta es para un archivo de medios
        if request.path.startswith(settings.MEDIA_URL):
            media_path = request.path[len(settings.MEDIA_URL):]
            media_full_path = os.path.join(settings.MEDIA_ROOT, media_path)
            # Check if the media file exists
            if not os.path.exists(media_full_path):
                html_template = loader.get_template('home/page-404.html')
                return HttpResponse(html_template.render(context, request))
            
            return serve(request, media_path, document_root=settings.MEDIA_ROOT)

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
