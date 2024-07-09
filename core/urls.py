# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.aulas.urls")),
    path("", include("apps.home.urls"))             
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# Manejadores de errores
handler404 = 'apps.home.views.error_404_view'
handler500 = 'apps.home.views.error_500_view'