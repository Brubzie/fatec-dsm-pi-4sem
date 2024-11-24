from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import datetime
from django.views.generic.edit import FormView
from .forms import LoginForm, RegisterForm, EditUserForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse_lazy


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


class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # Validações adicionais antes de salvar
        if not self.is_email_unique(form.cleaned_data.get("email")):
            form.add_error("email", "Este e-mail já está registrado.")
            return self.form_invalid(form)

        if not self.is_username_unique(form.cleaned_data.get("username")):
            form.add_error("username", "Este nome de usuário já está registrado.")
            return self.form_invalid(form)

        # Salvar o usuário se as validações passarem
        form.save()
        messages.success(self.request, "Cadastro realizado com sucesso! Faça login.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Exibe mensagens de erro caso o formulário seja inválido
        messages.error(self.request, "Por favor, corrija os erros no formulário.")
        return super().form_invalid(form)

    def is_email_unique(self, email):
        from django.contrib.auth.models import User

        return not User.objects.filter(email=email).exists()

    def is_username_unique(self, username):
        from django.contrib.auth.models import User

        return not User.objects.filter(username=username).exists()


class LoginView(FormView):
    """
    View para login de usuários.
    Renderiza o formulário de login e processa a submissão.
    """

    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user and user.is_active:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Credenciais inválidas.")
                return render(request, self.template_name, {"form": form})
        else:
            messages.error(request, "Erro no formulário. Verifique os dados.")
            return render(request, self.template_name, {"form": form})


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

class SocialView(View):
    template_name = 'social.html'

    def get(self, request):
        data = {'user': request.user}
        return render(request, self.template_name, data)
    
@login_required
def EditView(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../homeClient')
    else:
        form = EditUserForm(instance=request.user)
    
    return render(request, 'edit', {'form': form})