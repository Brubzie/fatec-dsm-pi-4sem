from django.urls import path
from .views import (
    IndexView,
    RegisterView,
    LoginView,
    HomeClientView,
    HistoryClientView,
    logout_view,
)

# Definindo os handlers de erro
handler404 = "core.views.handler404"
handler500 = "core.views.handler500"

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
    path("history/", HistoryClientView.as_view(), name="history"),
]
