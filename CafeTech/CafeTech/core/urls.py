from django.urls import path
from .views import IndexView, RegisterView, LoginView, HomeClientView, HistoryClientView, LogoutView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("home/", HomeClientView.as_view(), name="home_client"),
    path("history/", HistoryClientView.as_view(), name="history_client"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
