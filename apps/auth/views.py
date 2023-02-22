from django.contrib.auth.views import LoginView, LogoutView

from apps.auth.forms import LoginForm


class Login(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'


class Logout(LogoutView):
    pass
