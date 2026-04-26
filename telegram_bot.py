import logging
import asyncio
import sys
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import re
import os
from ftth_mcp_server import consultar_ruta_hilo, auditar_empalmes_criticos
from utils_plot import generate_plot
from ai_engine import ask_ai

# Forzar salida en UTF-8 para evitar errores de encoding en Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Cargar variables de entorno
load_dotenv()

# Configuración
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZED_CHAT_ID = int(os.getenv("TELEGRAM_AUTHORIZED_CHAT_ID", "0"))

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /start"""
    user_id = update.effective_user.id
    if user_id != AUTHORIZED_CHAT_ID:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f"Lo siento, no tienes acceso. Tu ID es {user_id}"
        )
        return
        
    mensaje = (
        "🤖 *FiberMind Analytics - Bot Activo*\n\n"
        "Puedo ayudarte a monitorear la red de Chiminangos.\n"
        "Comandos disponibles:\n"
        "🔍 /auditar - Busca fallas críticas en el Cable 1\n"
        "📊 /hilo [n] - Muestra la radiografía del hilo n\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode='Markdown')

async def auditar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /auditar"""
    if update.effective_user.id != AUTHORIZED_CHAT_ID: return

    await context.bot.send_message(chat_id=update.effective_chat.id, text="🔎 Ejecutando auditoría en base de datos real...")
    
    # Usamos nuestra herramienta de backend (umbral 0.2 dB)
    resultado = auditar_empalmes_criticos(0.2, id_cable=1)
    
    # Si el mensaje es muy largo, lo truncamos para Telegram
    if len(resultado) > 4000:
        resultado = resultado[:4000] + "\n\n...(Lista truncada por longitud)"
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resultado)

async def hilo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /hilo [número]"""
    if update.effective_user.id != AUTHORIZED_CHAT_ID: return

    if not context.args:
        await update.message.reply_text("Por favor, indica el número de hilo. Ej: /hilo 61")
        return

    try:
        id_hilo = int(context.args[0])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"📊 Generando radiografía del Hilo {id_hilo}...")
        
        resultado = consultar_ruta_hilo(1, id_hilo)
        
        # Generar y enviar gráfico
        plot_path = f"trace_{id_hilo}.png"
        img_path = generate_plot(1, id_hilo, plot_path)
        
        if img_path and os.path.exists(img_path):
            with open(img_path, 'rb') as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=resultado)
            os.remove(img_path) # Limpiar archivo temporal
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=resultado)
            if "hilo en uso" not in resultado:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="*(No se pudo generar la gráfica de la traza)*", parse_mode="Markdown")
        
    except ValueError:
        await update.message.reply_text("El ID de hilo debe ser un número entero.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes de texto libre (Lenguaje Natural)"""
    if update.effective_user.id != AUTHORIZED_CHAT_ID: return
    
    text = update.message.text.lower()
    
    # Buscar si el usuario pregunta por un hilo (ej: "muestra el hilo 123" o "hilo 61")
    match = re.search(r'hilo\s+(\d+)', text)
    if match:
        id_hilo = int(match.group(1))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"📊 Entendido, buscando radiografía del Hilo {id_hilo}...")
        resultado = consultar_ruta_hilo(1, id_hilo)
        
        # Generar y enviar gráfico
        plot_path = f"trace_{id_hilo}.png"
        img_path = generate_plot(1, id_hilo, plot_path)
        
        if img_path and os.path.exists(img_path):
            with open(img_path, 'rb') as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=resultado)
            os.remove(img_path)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=resultado)
            if "hilo en uso" not in resultado:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="*(No se pudo generar la gráfica de la traza)*", parse_mode="Markdown")
        return

    # Si menciona auditoría
    if 'audita' in text or 'revisa' in text:
        await auditar(update, context)
        return

    # RAZONAMIENTO CON IA: Si no coincide con nada de lo anterior, preguntar a Gemini
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        respuesta_ai = await ask_ai(update.message.text)
        await update.message.reply_text(respuesta_ai, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Lo siento, tuve un problema al razonar la respuesta: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    auditar_handler = CommandHandler('auditar', auditar)
    hilo_handler = CommandHandler('hilo', hilo)
    
    application.add_handler(start_handler)
    application.add_handler(auditar_handler)
    application.add_handler(hilo_handler)
    
    # Manejador para lenguaje natural (mensajes de texto que no son comandos)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    print("Bot de Telegram iniciado y esperando comandos...")
    application.run_polling()
