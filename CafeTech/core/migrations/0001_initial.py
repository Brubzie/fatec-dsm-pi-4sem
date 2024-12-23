# Generated by Django 5.1.3 on 2024-11-19 12:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(help_text='Informe o número no formato (99) 99999-9999 ou (99) 9999-9999.', max_length=15, verbose_name='Número de Telefone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Perfil do Usuário',
                'verbose_name_plural': 'Perfis dos Usuários',
                'ordering': ['user__username'],
            },
        ),
    ]
