from django.urls import include, path
from django.contrib.auth.views import LogoutView, PasswordResetView
from django_registration.backends.activation.views import RegistrationView

from users.forms import EmailPasswordResetForm, RegistrationForm
from users.views import create_user_account


urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('password_reset/',
         PasswordResetView.as_view(form_class=EmailPasswordResetForm),
         name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', RegistrationView.as_view(form_class=RegistrationForm), name='django_registration_register'),
    path('', include('django_registration.backends.activation.urls'))
]
