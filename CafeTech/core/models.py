from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)  # Biografia do usuário
    birth_date = models.DateField(blank=True, null=True)  # Data de nascimento
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Foto de perfil
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Número de telefone
    adimplencia = models.BooleanField(default=True)  # Situação de adimplência (pode ser True ou False)
    data_registro = models.DateTimeField(auto_now_add=True)  # Data de registro

    def __str__(self):
        return f'{self.user.username} Profile'
