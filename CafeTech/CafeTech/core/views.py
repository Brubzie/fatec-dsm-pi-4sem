from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


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
                return HttpResponseRedirect(reverse('index'))
        
        data = { 
            'form': form,
            'error': 'Usuário ou senha inválidos'
        }     
        return render(request, self.template_name, data)

class HomeClientView(View):
    template_name = 'homeClient.html'

    def get(self, request):
        return render(request, self.template_name)


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
