from django.urls import path
from django.conf.urls import handler404
from .views import (
    IndexView,
    RegisterView,
    LoginView,
    HomeClientView,
    HistoryClientView,
    LogoutView,
    SocialView,
    EditView,
    handler404,
    handler500,
)

# Definindo os handlers de erro
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("home/", HomeClientView.as_view(), name="home"),
    path("history/", HistoryClientView.as_view(), name="history_client"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("social/", SocialView.as_view(), name="social"),
    path("editPerfil/", EditView.as_view(), name="edit"),
]
