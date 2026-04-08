from django.urls import path

from users.views import site_config

urlpatterns = [
    path('config/', site_config, name='site-config'),
]
