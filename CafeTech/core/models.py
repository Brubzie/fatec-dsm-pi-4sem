from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Modelo para armazenar informações adicionais do usuário.
    Relaciona-se com o modelo padrão de User através de OneToOneField.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Usuário",
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Número de Telefone",
        help_text="Informe o número no formato (99) 99999-9999 ou (99) 9999-9999.",
    )

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"
        ordering = ["user__username"]  # Ordena pelo nome de usuário
