from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]

# Include package URLs if they exist
try:
    from wagtail_heelo_world import urls as package_urls

    urlpatterns.append(path("wagtail_heelo_world/", include(package_urls)))
except ImportError:
    pass

# Wagtail catch-all (must be last)
urlpatterns.append(path("", include(wagtail_urls)))

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
