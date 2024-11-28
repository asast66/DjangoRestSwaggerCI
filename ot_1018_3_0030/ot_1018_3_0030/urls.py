from django.contrib import admin
from django.urls import path
from app import views

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(title='test', default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', views.test),
    path('docs', schema_view.with_ui('swagger', cache_timeout=0)),
    path('another_test', views.another_test),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
