from django.urls import path
from wagtail.contrib.sitemaps.views import sitemap

from . import views


urlpatterns = [
    path('favicon.ico', views.favicon, name='favicon'),
    path('robots.txt', views.robots, name='robots'),
    path('sitemap.xml', sitemap, name='sitemap'),
]
