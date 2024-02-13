from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('backoffice/', admin.site.urls),
    path('api/auth', include('rest_framework.urls', namespace='rest_framework')),
    # Freight app
    path('api/v1/', include('core.freight.urls', namespace='freight')),
]
