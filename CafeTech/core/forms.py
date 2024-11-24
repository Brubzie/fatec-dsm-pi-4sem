from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    """
    Formulário de registro de novo usuário.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)  # Número de telefone
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=True)  # Data de nascimento

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number', 'birth_date']
        
        # Usando widgets para adicionar o ID e classe ao campo phone_number
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',  # Adicionando a classe do Bootstrap
                'id': 'phone_number'      # Definindo o ID
            })
        }

class EditUserForm(forms.ModelForm):
    """
    Formulário de edição de informações do usuário.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class EditUserProfileForm(forms.ModelForm):
    """
    Formulário de edição de informações adicionais do perfil do usuário.
    """
    bio = forms.CharField(widget=forms.Textarea, required=False)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    profile_picture = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)  # Adicionando telefone
    adimplencia = forms.BooleanField(required=False)  # Adicionando adimplência

    # O campo data_registro será preenchido automaticamente, então não precisa ser editável
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'profile_picture', 'phone_number', 'adimplencia']
