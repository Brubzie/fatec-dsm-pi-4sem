from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from django.views.generic.edit import FormView


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        data = {
            "user": request.user,
            "current_year": datetime.now().year,
            "YOUR_GOOGLE_CLIENT_ID": settings.YOUR_GOOGLE_CLIENT_ID,
        }
        return render(request, self.template_name, data)


class RegisterView(View):
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        context = kwargs
        context["YOUR_GOOGLE_CLIENT_ID"] = settings.YOUR_GOOGLE_CLIENT_ID
        return context

    def get(self, request):
        form = RegisterForm()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o usuário diretamente no banco
            messages.success(request, "Registro bem-sucedido! Faça login.")
            return redirect("login")
        else:
            messages.error(request, "Corrija os erros no formulário.")
        return render(request, self.template_name, self.get_context_data(form=form))


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("homeClient")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["YOUR_GOOGLE_CLIENT_ID"] = (
            settings.YOUR_GOOGLE_CLIENT_ID
        )  # Passe o client ID do Google
        return context

    def form_valid(self, form):
        """Se o formulário for válido, faça o login do usuário e redirecione"""
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            form.add_error(None, "Credenciais inválidas")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Se o formulário for inválido, renderize a página com os erros"""
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
                "error": form.errors,
            },
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
        if not messages.get_messages(request):
            messages.info(request, "Bem-vindo de volta!")
        return render(request, self.template_name, {"user": request.user})


class HistoryClientView(LoginRequiredMixin, View):
    login_url = "/login/"
    template_name = "historyClient.html"

    def get(self, request):
        return render(request, self.template_name)


@login_required(login_url="/login/")
def logout_view(request):
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


class google_login(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = SocialLoginSerializer
