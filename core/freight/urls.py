from django.urls import path, include
from rest_framework import routers
from core.freight import views


app_name = 'freight'

urlpatterns = [
    path('freight/', views.FreightApiView.as_view(), name='create_freight'),
]