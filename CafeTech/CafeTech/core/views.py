from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from CafeTech.settings import YOUR_GOOGLE_CLIENT_ID
from google.oauth2 import id_token
from google.auth.transport import requests
import json, time
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        data = {'user': request.user}
        return render(request, self.template_name, data)


class RegisterView(View):
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['YOUR_GOOGLE_CLIENT_ID'] = YOUR_GOOGLE_CLIENT_ID
        
        return context

    def get(self, request):
        data = {'form': RegisterForm()}
        return render(request, self.template_name, data)

    def post(self, request):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if username and password and confirm_password and password == confirm_password:
                user = User.objects.create_user(
                    username = username,
                    password = password
                )
                
                if user:
                    return HttpResponseRedirect(reverse('login'))
                
        data = {
            'form': form,
            'error': 'Usuário ou senha inválidos'
        }
        return render(request, self.template_name, {'form': form})

class LoginView(LoginView):
    template_name = 'login.html'

    def get(self, request):
        data = {'form': LoginForm()}
        return render(request, self.template_name, data)

    def post(self, request):
        form = LoginForm(data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
        
        data = { 
            'form': form,
            'error': 'Usuário ou senha inválidos'
        }     
        return render(request, self.template_name, data)

@method_decorator(login_required(login_url='/login/'), name='dispatch') # Redireciona quando o usuário não está logado
class HomeClientView(View):
    template_name = 'homeClient.html'

    def dispatch(self, request, *args, **kwargs):
        # Adiciona uma mensagem de aviso se o usuário não estiver autenticado
        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa estar logado para acessar esta página.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        messages.info(request, 'Bem-vindo de volta!')
        
        return render(request, self.template_name, {'user': request.user})


class HistoryClientView(View):
    template_name = 'historyClient.html'

    def get(self, request):
        return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    
def handler404(request, *args, **argv):
    response = render(request, '404.html', {})
    response.status_code = 404
    
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html', {})
    response.status_code = 500
    
    return response

@csrf_exempt
def google_login(request):
    template_name = 'homeClient.html'
    
    time.sleep(3)
    token = request.body
    token = token.decode('utf-8').encode('windows-1252').decode('utf-8')
    token = json.loads(token)
    token = token['id_token']
    
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), YOUR_GOOGLE_CLIENT_ID)
        userid = idinfo['sub']
        print(idinfo)
    except ValueError:
        pass
        
    return render(request, template_name)
