from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import django
from django.conf import settings
import os
from dotenv import load_dotenv

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CafeTech.settings')
django.setup()

load_dotenv()

TOKEN = os.getenv("TOKEN")

from core.models import UserProfile

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Olá! Use o comando /consulta_nome ou /consulta_email para verificar adimplência."
    )

async def consulta_nome(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("Por favor, forneça um nome de usuário.")
        return

    nome = " ".join(context.args)
    try:
        user_profile = UserProfile.objects.get(user__username=nome)
        if user_profile.adimplencia:
            await update.message.reply_text(f"O usuário {nome} está **adimplente**.")
        else:
            await update.message.reply_text(f"O usuário {nome} está **inadimplente**.")
    except UserProfile.DoesNotExist:
        await update.message.reply_text("Usuário não encontrado.")

async def consulta_email(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("Por favor, forneça um email.")
        return

    email = " ".join(context.args)
    try:
        user_profile = UserProfile.objects.get(user__email=email)
        if user_profile.adimplencia:
            await update.message.reply_text(f"O email {email} está **adimplente**.")
        else:
            await update.message.reply_text(f"O email {email} está **inadimplente**.")
    except UserProfile.DoesNotExist:
        await update.message.reply_text("Email não encontrado.")

def main():
    application = Application.builder().token(TOKEN).build()

    # Adiciona os handlers diretamente ao application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("consulta_nome", consulta_nome))
    application.add_handler(CommandHandler("consulta_email", consulta_email))

    # Inicia o polling
    application.run_polling()

if __name__ == "__main__":
    main()
