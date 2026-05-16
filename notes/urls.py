from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include(("notes.urls", "notes"), namespace="notes"),
    ),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

# Customize Django admin panel
admin.site.site_header = "SmartNotes Admin"
admin.site.site_title = "SmartNotes Portal"
admin.site.index_title = "Welcome to SmartNotes Dashboard"
