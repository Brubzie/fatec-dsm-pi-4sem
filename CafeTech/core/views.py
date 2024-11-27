from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import datetime
from .forms import EditUserForm
from .forms import RegisterForm
from .models import UserProfile
from django.db import IntegrityError, transaction
import csv

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
            try:
                # Usando uma transação para consistência
                with transaction.atomic():
                    # Criando o usuário
                    user = form.save()

                    # Obtendo os dados adicionais do formulário
                    phone_number = form.cleaned_data.get('phone_number')
                    birth_date = form.cleaned_data.get('birth_date')

                    # Criando ou recuperando o perfil do usuário
                    profile, created = UserProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'phone_number': phone_number,
                            'birth_date': birth_date,
                            'adimplencia': True,
                        }
                    )

                    # Logando o usuário
                    login(request, user)

                    # Redirecionando para a página inicial
                    return redirect('index')
            except IntegrityError:
                form.add_error(None, "Erro ao criar o perfil. Já existe um usuário associado.")
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

# Verificar se o usuário é administrador
def is_admin(user):
    return user.is_staff


# View para exibir relatório de adimplentes
@login_required
@user_passes_test(is_admin)  # Apenas para admins
def relatorio_adimplentes(request):
    adimplentes = UserProfile.objects.filter(adimplencia=True)

    # Retornar uma página HTML com os dados
    return render(request, 'relatorios/adimplentes.html', {'adimplentes': adimplentes})


# View para gerar relatório de inadimplentes em CSV
@login_required
@user_passes_test(is_admin)  # Apenas para admins
def relatorio_inadimplentes_csv(request):
    inadimplentes = UserProfile.objects.filter(adimplencia=False)

    # Gerar arquivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inadimplentes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Email', 'Telefone', 'Data de Registro'])

    for user in inadimplentes:
        writer.writerow([user.user.username, user.user.email, user.phone_number, user.data_registro])

    return response