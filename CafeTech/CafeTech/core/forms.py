from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email',
        }),
        label='Email'
    )
    
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu número de telefone',
        }),
        label='Número de Telefone'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
        }),
        label='Senha',
        help_text='A senha deve conter pelo menos 8 caracteres, incluindo números, letras maiúsculas e minúsculas, e caracteres especiais.'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha',
        }),
        label='Confirme a Senha'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Usuário',
            'password': 'Senha',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu usuário',
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise ValidationError('O nome de usuário deve ter pelo menos 4 caracteres.')
        if username.isdigit():
            raise ValidationError('O nome de usuário não pode conter apenas números.')
        if re.search(r'[\W_]', username):
            raise ValidationError('O nome de usuário não deve conter caracteres especiais.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('A senha deve ter no mínimo 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('A senha deve conter pelo menos um número.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('A senha deve conter pelo menos um caractere especial.')
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('As senhas não coincidem', code='password_mismatch')
        return confirm_password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_regex = re.compile(r'^\(\d{2}\)\s?\d{4,5}-\d{4}$')
        if not phone_regex.match(phone_number):
            raise ValidationError('O número de telefone deve estar no formato (99) 99999-9999 ou (99) 9999-9999.')
        return phone_number


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário',
        })
    )
    
    password = forms.CharField(
        max_length=128, 
        required=True, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Nome de usuário ou senha incorretos.')
        return cleaned_data
