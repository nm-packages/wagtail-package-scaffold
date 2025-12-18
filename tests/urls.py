from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("", include(wagtail_urls)),
]

# Include package URLs if they exist
try:
    from wagtail_heelo_world import urls as package_urls

    urlpatterns.insert(0, path("wagtail_heelo_world/", include(package_urls)))
except ImportError:
    pass
