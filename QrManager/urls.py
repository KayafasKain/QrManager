"""QrManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import routers

from qr_manager.views_api import QrCodeViewSet, QrCodeScanViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="QrManager API",
      default_version='v1',
      description="Qr manager api references",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@qrcode.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

router = routers.DefaultRouter()
router.register(r'code', QrCodeViewSet, basename='code')
router.register(r'code/scan', QrCodeScanViewSet, basename='code-scan')

urlpatterns = [
    path('qr/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    url(
        r'^(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    url(
        r'',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
]
