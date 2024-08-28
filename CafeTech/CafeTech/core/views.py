from django.shortcuts import render
from django.views import View

class IndexView(View):
    template_name = "index.html"
    
    def get(self, request):
        return render(request, self.template_name)

class RegisterView(View):
    template_name = "register.html"
    
    def get(self, request):
        return render(request, self.template_name)

class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)
    
class HomeClientView(View):
    template_name = "homeClient.html"

    def get(self, request):
        return render(request, self.template_name)
    
class HistoryClientView(View):
    template_name = "historyClient.html"

    def get(self, request):
        return render(request, self.template_name)
    
class LogoutView(View):
    template_name = "logout.html"

    def get(self, request):
        return render(request, self.template_name)