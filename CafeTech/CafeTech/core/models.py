from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, verbose_name='Número de Telefone')

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
