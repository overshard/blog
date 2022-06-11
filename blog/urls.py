from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from pages import urls as pages_urls

urlpatterns = [
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path("", include(pages_urls)),

    re_path(r"", include(wagtail_urls)),
]


if settings.DEBUG:
    urlpatterns.append(path("403/", TemplateView.as_view(template_name="403.html")))
    urlpatterns.append(path("404/", TemplateView.as_view(template_name="404.html")))
    urlpatterns.append(path("500/", TemplateView.as_view(template_name="500.html")))
    urlpatterns += static("media/", document_root=settings.MEDIA_ROOT)
