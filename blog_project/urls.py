from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="Interview Task - Blog API",
      default_version='v1',
      description="API documentation for the Blog app",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/blog/', include('blog.urls')),

    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
