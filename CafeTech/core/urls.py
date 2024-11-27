from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    IndexView,
    register,
    HomeClientView,
    logout_view,
    SocialView,
    EditView,
)
from . import views

# URLs principais
urlpatterns = [
    # Página inicial
    path('', IndexView.as_view(), name='index'),
    # Rotas de autenticação
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('social/', SocialView.as_view(), name='social'),
    path('relatorio/adimplentes/', views.relatorio_adimplentes, name='relatorio_adimplentes'),
    path('relatorio/inadimplentes/csv/', views.relatorio_inadimplentes_csv, name='relatorio_inadimplentes_csv'),
    # Páginas do cliente
    path('home/', HomeClientView.as_view(), name='home'),
    path('editPerfil/', EditView, name='edit'),
]
