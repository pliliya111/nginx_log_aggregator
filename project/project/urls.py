from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from log_parser.views import LogParserAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Nginx Log API",
        default_version="v1",
        description="API для агрегации логов Nginx",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@nginxlog.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/logs/", LogParserAPIView.as_view()),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
