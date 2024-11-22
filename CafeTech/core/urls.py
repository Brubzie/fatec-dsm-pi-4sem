from django.urls import path
from .views import (
    IndexView,
    RegisterView,
    LoginView,
    HomeClientView,
    SettingsClientView,
    logout_view,
)

# URLs principais
urlpatterns = [
    # Página inicial
    path("", IndexView.as_view(), name="index"),
    # Rotas de autenticação
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    # Páginas do cliente
    path("home/", HomeClientView.as_view(), name="home"),
    path("settings/", SettingsClientView.as_view(), name="settings"),
]
