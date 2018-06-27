from django.urls import path

from . import views

urlpatterns = [
    # ex: /eqprecog/upload
    path('upload', views.upload, name='upload'),
]
