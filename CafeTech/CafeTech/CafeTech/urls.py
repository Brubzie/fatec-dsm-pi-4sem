from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),  # Inclui as URLs do app 'core'
    path("rest-auth/", include("rest_auth.urls")),  # Inclui as URLs de autenticação
    path(
        "rest-auth/registration/", include("rest_auth.registration.urls")
    ),  # Inclui as URLs de registro
]
