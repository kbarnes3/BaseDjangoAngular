"""NewDjangoSite URL Configuration"""
from django.contrib import admin
from django.urls import path, include

from common.views import hello_world

urlpatterns = [
    path('', hello_world, name='landing_page'),

    path('admin/', admin.site.urls),

    path('_allauth/', include('allauth.headless.urls')),
]
