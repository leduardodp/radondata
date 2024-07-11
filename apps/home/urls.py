from django.urls import path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

]
