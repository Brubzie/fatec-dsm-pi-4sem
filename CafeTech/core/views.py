from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import datetime
from django.views.generic.edit import FormView
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User


class IndexView(View):
    """
    Página inicial do sistema.
    Exibe informações básicas.
    """

    template_name = "index.html"

    def get(self, request):
        context = {
            "user": request.user,
            "current_year": datetime.now().year,
        }
        return render(request, self.template_name, context)


class RegisterView(View):
    """
    View para registro de novos usuários.
    Renderiza o formulário de registro e processa a submissão.
    """

    template_name = "register.html"

    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, request):
        form = RegisterForm()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        user = User.objects.filter(username=username).first()

        if user:
            messages.error(request, "já existe um usuario com esse nome")
            return render(request, "login.html")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone_number,
            )
            user.save()
            messages.success(request, "Registro bem-sucedido! Faça login.")
            return redirect("login")


class LoginView(FormView):
    """
    View para login de usuários.
    Valida as credenciais e autentica o usuário no sistema.
    """

    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("homeClient")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user:
            login(self.request, user)
            messages.success(self.request, "Login realizado com sucesso!")
            return redirect(self.get_success_url())
        else:
            # Adiciona um erro geral sem referência a campos específicos
            messages.error(self.request, "Credenciais inválidas")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # O Django já lida com a renderização dos erros automaticamente
        return render(self.request, self.template_name, {"form": form})


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class HomeClientView(View):
    """
    Página inicial do cliente autenticado.
    Exibe uma mensagem de boas-vindas.
    """

    template_name = "homeClient.html"

    def get(self, request):
        if not messages.get_messages(request):
            messages.info(request, "Bem-vindo de volta!")
        return render(request, self.template_name, {"user": request.user})


class SettingsClientView(LoginRequiredMixin, View):
    """
    Página de histórico do cliente.
    Apenas acessível por usuários autenticados.
    """

    login_url = "/login/"
    template_name = "historyClient.html"

    def get(self, request):
        return render(request, self.template_name)


@login_required(login_url="/login/")
def logout_view(request):
    """
    View para logout do sistema.
    Redireciona para a página de login após encerrar a sessão do usuário.
    """
    logout(request)
    messages.info(request, "Você foi desconectado com sucesso.")
    return HttpResponseRedirect(reverse("login"))
