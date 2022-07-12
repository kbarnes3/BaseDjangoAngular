from django.urls import include, path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordResetView

from users.forms import EmailPasswordResetForm
from users.views import create_user_account


urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='auth_logout'),
    path('password/reset/',
         PasswordResetView.as_view(
            form_class=EmailPasswordResetForm,
            success_url=reverse_lazy('auth_password_reset_done')),
         name='auth_password_reset'),
    path('', include('registration.backends.default.urls')),
    path('signup/', create_user_account, name='create_user_account')
]
