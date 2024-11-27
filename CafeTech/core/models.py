from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)  # Biografia do usuário
    birth_date = models.DateField(blank=True, null=True)  # Data de nascimento
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Foto de perfil
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Número de telefone
    adimplencia = models.BooleanField(default=True)  # Situação de adimplência (pode ser True ou False)
    data_registro = models.DateTimeField(auto_now_add=True)  # Data de registro

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'Perfil de: {self.user.username}'
    
    @classmethod
    def verificar_adimplencia(nome=None, email=None):
        try:
            if nome:
                usuario = User.objects.get(username=nome)
            elif email:
                usuario = User.objects.get(email=email)
            else:
                return "Por favor, forneça um nome ou email válido."
            
            perfil = usuario.profile
            if perfil.adimplencia:
                return f"Usuário {usuario.username} está **adimplente**."
            else:
                return f"Usuário {usuario.username} está **inadimplente**."
        except User.DoesNotExist:
            return "Usuário não encontrado."
        except Exception as e:
            return f"Ocorreu um erro: {e}"
