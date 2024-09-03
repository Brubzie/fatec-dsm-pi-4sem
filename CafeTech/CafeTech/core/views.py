from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from .forms import RegisterForm
from django.contrib.auth.views import LoginView

class IndexView(View):
    template_name = 'index.html'
    
    def get(self, request):
        return render(request, self.template_name)

class RegisterView(View):
    template_name = 'register.html'
    
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')  # Redireciona para a página inicial ou outra página de sua escolha
        return render(request, self.template_name, {'form': form})

class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        # Se o usuário já está autenticado, redireciona para a página de destino
        if self.request.user.is_authenticated:
            return self.handle_no_permission()
        # Caso contrário, renderiza o template com o formulário de login
        return render(request, self.template_name, {'form': self.get_form()})
    
class HomeClientView(View):
    template_name = 'homeClient.html'

    def get(self, request):
        return render(request, self.template_name)
    
class HistoryClientView(View):
    template_name = 'historyClient.html'

    def get(self, request):
        return render(request, self.template_name)
    
def logout(request):
    auth_logout(request)
    return redirect('index')