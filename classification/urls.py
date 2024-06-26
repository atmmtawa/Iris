from django.urls import path, include
from . import views

# https://docs.djangoproject.com/en/4.0/ref/templates/language/#id1

appname = "classification"
urlpatterns = [
    path('', views.home, name="home"),
    path('classiffier/', views.classifier, name="classiffier"),
    # path('', views.predict_view, name ="predict_view"),

    path('upload/', views.upload_csv, name='upload_csv'),
    path('predict-csv/', views.predict_csv, name='predict_csv'),
    path('predict-pdf/', views.predict_pdf, name='predict_pdf'),
]
