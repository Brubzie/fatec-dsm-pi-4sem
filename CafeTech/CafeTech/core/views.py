from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from CafeTech.settings import YOUR_GOOGLE_CLIENT_ID
from google.oauth2 import id_token
from google.auth.transport import requests
import json

class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        data = {'user': request.user}
        return render(request, self.template_name, data)

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        data = {'form': RegisterForm()}
        return render(request, self.template_name, data)

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já existe.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email já está em uso.')
            else:
                User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                messages.success(request, 'Registro bem-sucedido! Faça login.')
                return redirect('login')
        
        return render(request, self.template_name, {'form': form})

class LoginView(DjangoLoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_form_kwargs(self):
        """Retorna os argumentos que serão passados para o formulário."""
        kwargs = super().get_form_kwargs()
        # Remove o request dos kwargs se estiver presente
        kwargs.pop('request', None)
        return kwargs

    def form_valid(self, form):
        """Se o formulário for válido, faça o login do usuário e redirecione"""
        login(self.request, form.get_user())
        return HttpResponseRedirect(reverse('homeClient'))

    def form_invalid(self, form):
        """Se o formulário for inválido, renderize a página com os erros"""
        return render(self.request, self.template_name, {
            'form': form,
            'error': 'Usuário ou senha inválidos'
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class HomeClientView(View):
    template_name = 'homeClient.html'

    def get(self, request):
        messages.info(request, 'Bem-vindo de volta!')
        return render(request, self.template_name, {'user': request.user})

class HistoryClientView(LoginRequiredMixin, View):
    template_name = 'historyClient.html'

    def get(self, request):
        return render(request, self.template_name)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Você foi desconectado com sucesso.')
        return HttpResponseRedirect(reverse('login'))

def handler404(request, *args, **argv):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response

def google_login(request):
    template_name = 'homeClient.html'
    token = request.body.decode('utf-8')
    token = json.loads(token).get('id_token')

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), YOUR_GOOGLE_CLIENT_ID)
        userid = idinfo['sub']
        email = idinfo['email']

        user, created = User.objects.get_or_create(username=userid, defaults={'email': email})
        if created:
            user.set_password(User.objects.make_random_password())  # Define uma senha aleatória
            user.save()
        
        login(request, user)
        messages.success(request, 'Login com Google realizado com sucesso!')
        return HttpResponseRedirect(reverse('homeClient'))
        
    except ValueError:
        messages.error(request, 'Falha na autenticação do Google.')
        return render(request, template_name)
