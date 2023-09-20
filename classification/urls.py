from django.urls import path, include
from . import views

# https://docs.djangoproject.com/en/4.0/ref/templates/language/#id1

appname = "classification"
urlpatterns = [

    path('', views.classifier, name="classiffier"),
    # path('', views.predict_view, name ="predict_view"),

    path('upload-csv/', views.upload_csv, name='upload_csv'),
]
