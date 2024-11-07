from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
import json


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        data = {
            "user": request.user,
            "current_year": datetime.now().year,
        }
        return render(request, self.template_name, data)


class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        form = RegisterForm()
        context = {
            "form": form,
            "YOUR_GOOGLE_CLIENT_ID": settings.YOUR_GOOGLE_CLIENT_ID,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")

            # Verifica se as senhas coincidem
            if User.objects.filter(username=username).exists():
                messages.error(request, "Nome de usuário já existe.")
            # Verifica se o email é válido
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email já está em uso.")
            # Verifica se o número de telefone é válido
            elif User.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "Número de telefone já está em uso.")
            else:
                User.objects.create_user(
                    username=username, password=password, email=email
                )
                messages.success(request, "Registro bem-sucedido! Faça login.")
                return redirect("login")

        return render(request, self.template_name, {"form": form})


class LoginView(DjangoLoginView):
    template_name = "login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["YOUR_GOOGLE_CLIENT_ID"] = (
            settings.YOUR_GOOGLE_CLIENT_ID
        )  # Passe o client ID do Google
        return context

    def get_form_kwargs(self):
        """Retorna os argumentos que serão passados para o formulário."""
        kwargs = super().get_form_kwargs()
        # Remove o request dos kwargs se estiver presente
        kwargs.pop("request", None)
        return kwargs

    def form_valid(self, form):
        """Se o formulário for válido, faça o login do usuário e redirecione"""
        login(self.request, form.get_user())
        return HttpResponseRedirect(reverse("homeClient"))

    def form_invalid(self, form):
        """Se o formulário for inválido, renderize a página com os erros"""
        return render(
            self.request,
            self.template_name,
            {"form": form, "error": "Usuário ou senha inválidos"},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class HomeClientView(View):
    template_name = "homeClient.html"

    def get(self, request):
        messages.info(request, "Bem-vindo de volta!")
        return render(request, self.template_name, {"user": request.user})


class HistoryClientView(LoginRequiredMixin, View):
    template_name = "historyClient.html"

    def get(self, request):
        return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "Você foi desconectado com sucesso.")
        return HttpResponseRedirect(reverse("login"))


def handler404(request):
    response = render(request, "404.html", {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, "500.html", {})
    response.status_code = 500
    return response


def google_login(self, request):
    if request.method == 'POST':
        token = json.loads(request.body.decode('utf-8')).get('id_token')

        try:
            # Verifica o token do Google
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.YOUR_GOOGLE_CLIENT_ID
            )

            userid = idinfo['sub']
            email = idinfo.get('email')

            # Tenta obter ou criar o usuário
            user, created = User.objects.get_or_create(
                username=userid, defaults={'email': email}
            )

            # Caso o usuário tenha sido criado, define uma senha aleatória
            if created:
                user.set_password(User.objects.make_random_password())
                user.save()

            # Realiza o login do usuário
            login(request, user)
            messages.success(request, "Login com Google realizado com sucesso!")

            # Redireciona para a página inicial do usuário
            return JsonResponse({"message": "Login realizado com sucesso!"})

        except ValueError:
            # Caso o token seja inválido
            return JsonResponse({"error": "Falha na autenticação do Google"}, status=400)

