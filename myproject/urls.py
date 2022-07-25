from django.contrib import admin
from django.urls import path , include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from myproject.settings import DEBUG
from django.urls.conf import re_path
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1.0',
      description="Api description",
      contact=openapi.Contact(email="mahmudul.hassan240@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
#    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('agent/', include('agent.urls', namespace="agent")),
]

urlpatterns += [path('api-auth/', include('rest_framework.urls')),]
if DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]