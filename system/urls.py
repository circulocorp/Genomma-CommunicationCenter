from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('env/backoffice/', admin.site.urls),
    path('env/api/auth', include('rest_framework.urls', namespace='rest_framework')),
    # Freight app
    path('env/api/v1/', include('core.freight.urls', namespace='freight')),
]
