from pathlib import Path
import os
import environ

# Configuração de BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializando o django-environ
env = environ.Env(
    DEBUG=(bool, True)  # Define DEBUG como booleano com valor padrão True
)

# Leia o .env
environ.Env.read_env(os.path.join(BASE_DIR, "CafeTech", ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")  # Carrega o valor de DEBUG

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# Definição de Aplicativos
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "core",
    # Django Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env.str("YOUR_GOOGLE_CLIENT_ID", ""),
            "secret": env.str("GOOGLE_SECRET_KEY", ""),
        },
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Middleware Account
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "CafeTech.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Django Allauth
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "CafeTech.wsgi.application"

# Database
DATABASES = {
    "default": env.db(default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3"))
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Configuração de Caches (Redis como exemplo)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    },
    "redis": env.cache_url(
        "REDIS_URL", default="redis://127.0.0.1:6379/1"
    ),  # Use o valor padão para Redis
}

# Internacionalização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Tipo de campo de chave primária padrão
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configurações de autenticação
LOGIN_REDIRECT_URL = "/"  # Redireciona para a página inicial após o login
LOGOUT_REDIRECT_URL = "/login/"  # Redireciona para a página de login após o logout
LOGIN_URL = "/login/"

# Adiciona '/' no final dos urls que não o tiverem
APPEND_SLASH = True

# Configuração de política de segurança para pop-ups cross-origin
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
