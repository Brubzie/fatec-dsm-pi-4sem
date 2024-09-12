from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"}),
        label="Senha",
        help_text="A senha deve conter pelo menos 8 caracteres, incluindo números, letras maiúsculas e minúsculas, e caracteres especiais."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirme sua senha"}),
        label="Confirme a Senha"
    )

    class Meta:
        model = User
        fields = ["username", "password"]
        labels = {
            "username": "Usuário",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Digite seu usuário"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        
        # Verificar se o username tem no mínimo 4 caracteres
        if len(username) < 4:
            raise ValidationError("O nome de usuário deve ter pelo menos 4 caracteres.")
        
        # Verificar se o username contém apenas números
        if username.isdigit():
            raise ValidationError("O nome de usuário não pode conter apenas números.")
        
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # Aqui você pode adicionar validações de senha, se desejar
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("As senhas não coincidem", code="password_mismatch")
        return confirm_password
