from django.urls import path, include
from . import views

# https://docs.djangoproject.com/en/4.0/ref/templates/language/#id1


urlpatterns = [

    path('', views.classiffier, name ="classiffier"),
]