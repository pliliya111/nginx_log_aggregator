from django.contrib import admin

from .models import NginxLog


@admin.register(NginxLog)
class NginxLogAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "date",
        "http_method",
        "uri",
        "response_code",
        "response_size",
    )
    search_fields = ("ip_address", "http_method", "uri")
    list_filter = ("http_method", "response_code")
