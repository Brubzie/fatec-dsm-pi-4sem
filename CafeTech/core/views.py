from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import datetime
from .forms import EditUserForm
from .forms import RegisterForm
from .models import UserProfile


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


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Criando o usuário
            user = form.save()

            # Obtendo os dados adicionais do formulário
            phone_number = form.cleaned_data.get('phone_number')
            birth_date = form.cleaned_data.get('birth_date')

            # Criando o perfil de usuário
            profile = UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                birth_date=birth_date,
                adimplencia=True,  # Definindo o padrão de adimplência como True para o novo usuário
            )

            # Logando o usuário
            login(request, user)
            
            # Redirecionando para a página inicial ou outra página de sua escolha
            return redirect('index')  
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class HomeClientView(View):
    """
    Página inicial do cliente autenticado.
    Exibe uma mensagem de boas-vindas.
    """

    template_name = "homeClient.html"

    def get(self, request):
        if not messages.get_messages(request):
            messages.info(request, f"Bem-vindo de volta {request.user.username}!")
        return render(request, self.template_name, {"user": request.user})

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
            # Adicionando uma mensagem de sucesso
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('homeClient')  # Usando a função reverse para redirecionamento
        else:
            # Adicionando uma mensagem de erro caso o formulário seja inválido
            messages.error(request, 'Ocorreu um erro ao atualizar seu perfil. Verifique os campos e tente novamente.')
    else:
        form = EditUserForm(instance=request.user)
    
    return render(request, 'editPerfil.html', {'form': form})
