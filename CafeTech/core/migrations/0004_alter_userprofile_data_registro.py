# Generated by Django 5.1.2 on 2024-11-26 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofile_adimplencia_userprofile_data_registro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='data_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]