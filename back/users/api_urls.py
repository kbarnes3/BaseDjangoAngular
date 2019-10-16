from django.urls import path
from users.views import logged_in_api


urlpatterns = [
    path('logged_in/', logged_in_api),
]
