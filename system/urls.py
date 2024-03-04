from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for your project",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('env/backoffice/', admin.site.urls),
    path('env/api/auth', include('rest_framework.urls', namespace='rest_framework')),
    # Freight app
    path('env/api/v1/', include('core.freight.urls', namespace='freight')),
    # Swagger
    path('env/api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Token
    path('env/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('env/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
