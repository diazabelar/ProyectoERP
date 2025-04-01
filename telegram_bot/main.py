import logging
import json
import time
import socket
import urllib.request
import urllib.error
import requests
from telegram import Update, ParseMode, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.request import Request
import paho.mqtt.client as mqtt
from config import *

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cliente MQTT global
mqtt_client = None

# Variable global para almacenar el updater de Telegram
telegram_updater = None

def check_internet_connection():
    """Verifica si hay conexión a Internet"""
    try:
        # Intentar conectar a Google DNS para verificar conectividad
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        pass
    
    try:
        # Intentar con la API de Google como alternativa
        urllib.request.urlopen("https://www.google.com", timeout=5)
        return True
    except urllib.error.URLError:
        pass
    
    return False

def check_telegram_api_access():
    """Verifica si se puede acceder a la API de Telegram"""
    try:
        response = requests.get("https://api.telegram.org", timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except:
        return False

def on_mqtt_connect(client, userdata, flags, rc, properties=None):
    """Callback cuando se conecta al broker MQTT (compatible con MQTTv5)"""
    if rc == 0:
        logger.info("Conectado al broker MQTT")
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
    else:
        logger.error(f"Error de conexión MQTT con código {rc}")

def on_mqtt_message(client, userdata, msg):
    """Callback cuando se recibe un mensaje MQTT"""
    try:
        payload = msg.payload.decode('utf-8')
        logger.info(f"Mensaje MQTT recibido en {msg.topic}: {payload}")
        
        # Intentar procesar como JSON
        try:
            data = json.loads(payload)
            
            # Si tiene un destinatario específico
            if "chat_id" in data and "message" in data:
                send_telegram_message(data["chat_id"], data["message"])
            else:
                # Enviar al administrador si no hay destinatario específico
                if ADMIN_CHAT_ID:
                    message_text = f"📩 *Mensaje MQTT recibido*\n\n📌 Tema: `{msg.topic}`\n\n📝 Contenido:\n```\n{payload}\n```"
                    send_telegram_message(ADMIN_CHAT_ID, message_text, parse_mode=ParseMode.MARKDOWN)
        except json.JSONDecodeError:
            # Si no es JSON, enviar el mensaje en crudo
            if ADMIN_CHAT_ID:
                message_text = f"📩 *Mensaje MQTT recibido*\n\n📌 Tema: `{msg.topic}`\n\n📝 Contenido:\n{payload}"
                send_telegram_message(ADMIN_CHAT_ID, message_text, parse_mode=ParseMode.MARKDOWN)
            
    except Exception as e:
        logger.error(f"Error procesando mensaje MQTT: {e}")

def send_telegram_message(chat_id, text, parse_mode=None):
    """Envía un mensaje a través del bot de Telegram"""
    if telegram_updater and telegram_updater.bot:
        try:
            telegram_updater.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
        except Exception as e:
            logger.error(f"Error enviando mensaje de Telegram: {e}")

def publish_mqtt_message(topic, message):
    """Publica un mensaje en un tema MQTT"""
    if mqtt_client and mqtt_client.is_connected():
        try:
            mqtt_client.publish(topic, message)
            logger.info(f"Mensaje publicado en MQTT {topic}: {message}")
            return True
        except Exception as e:
            logger.error(f"Error publicando en MQTT: {e}")
    else:
        logger.error("Cliente MQTT no conectado")
    return False

def start(update: Update, context: CallbackContext) -> None:
    """Comando /start - Inicia la interacción con el bot"""
    user = update.effective_user
    update.message.reply_text(f'¡Hola {user.first_name}! Soy un bot de Telegram que se integra con MQTT.\n\n'
                              f'Usa /help para ver los comandos disponibles.')
    
    # Publicar evento de inicio en MQTT
    user_info = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "chat_id": update.effective_chat.id,
        "event": "start"
    }
    publish_mqtt_message(f"{MQTT_TOPIC_BASE}/events", json.dumps(user_info))

def help_command(update: Update, context: CallbackContext) -> None:
    """Comando /help - Muestra la ayuda"""
    help_text = (
        "📚 *Comandos disponibles*:\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar este mensaje de ayuda\n"
        "/subscribe tema - Suscribirse a un tema MQTT\n"
        "/publish tema mensaje - Publicar un mensaje en un tema MQTT\n"
        "/status - Ver estado de la conexión MQTT\n\n"
        "También puedes enviar cualquier mensaje y se publicará en "
        f"el tema MQTT predeterminado: `{TOPIC_OUTGOING}`"
    )
    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

def subscribe_command(update: Update, context: CallbackContext) -> None:
    """Comando /subscribe - Se suscribe a un tema MQTT específico"""
    if not context.args:
        update.message.reply_text("❌ Por favor especifica un tema MQTT. Ejemplo: /subscribe casa/sala/temperatura")
        return
    
    topic = context.args[0]
    
    if mqtt_client and mqtt_client.is_connected():
        try:
            mqtt_client.subscribe(topic)
            update.message.reply_text(f"✅ Suscrito al tema MQTT: `{topic}`", parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            update.message.reply_text(f"❌ Error al suscribirse: {str(e)}")
    else:
        update.message.reply_text("❌ Cliente MQTT no conectado")

def publish_command(update: Update, context: CallbackContext) -> None:
    """Comando /publish - Publica un mensaje en un tema MQTT específico"""
    if len(context.args) < 2:
        update.message.reply_text("❌ Por favor especifica un tema y un mensaje. Ejemplo: /publish casa/sala/luz on")
        return
    
    topic = context.args[0]
    message = ' '.join(context.args[1:])
    
    if publish_mqtt_message(topic, message):
        update.message.reply_text(f"✅ Mensaje publicado en `{topic}`", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("❌ No se pudo publicar el mensaje")

def status_command(update: Update, context: CallbackContext) -> None:
    """Comando /status - Muestra el estado de la conexión MQTT"""
    if mqtt_client and mqtt_client.is_connected():
        update.message.reply_text(
            f"✅ *Conectado al broker MQTT*\n"
            f"📡 Broker: `{MQTT_BROKER}:{MQTT_PORT}`\n"
            f"🔖 ID Cliente: `{MQTT_CLIENT_ID}`\n"
            f"🔄 Tema base: `{MQTT_TOPIC_BASE}`",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("❌ No conectado al broker MQTT")

def handle_message(update: Update, context: CallbackContext) -> None:
    """Maneja los mensajes normales (no comandos)"""
    message = update.message.text
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    # Crear un objeto con información sobre el mensaje
    message_data = {
        "chat_id": chat_id,
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "message": message,
        "timestamp": time.time()
    }
    
    # Publicar el mensaje en MQTT
    if publish_mqtt_message(TOPIC_OUTGOING, json.dumps(message_data)):
        update.message.reply_text("✅ Mensaje enviado a MQTT")
    else:
        update.message.reply_text("❌ No se pudo enviar el mensaje a MQTT")

def main() -> None:
    """Función principal que inicia el bot y la conexión MQTT"""
    global mqtt_client, telegram_updater
    
    # Verificar que los tokens necesarios estén disponibles
    if not TELEGRAM_TOKEN:
        logger.error("Token de Telegram no encontrado. Configure la variable TELEGRAM_TOKEN en el archivo .env")
        return
    
    # Verificar conexión a Internet
    if not check_internet_connection():
        logger.error("No hay conexión a Internet. Verifique su conexión de red.")
        return
        
    # Inicializar la conexión MQTT
    try:
        # Usar el constructor client con version 5 para evitar el mensaje de deprecación
        mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv5)
        
        # Configurar callbacks
        mqtt_client.on_connect = on_mqtt_connect
        mqtt_client.on_message = on_mqtt_message
        
        # Configurar credenciales si están disponibles
        if MQTT_USERNAME and MQTT_PASSWORD:
            mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        
        # Conectar al broker MQTT
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Iniciar el loop MQTT en un hilo separado
        mqtt_client.loop_start()
        logger.info(f"Iniciando conexión MQTT a {MQTT_BROKER}:{MQTT_PORT}")
        
    except Exception as e:
        logger.error(f"Error al inicializar MQTT: {e}")
    
    # Inicializar el bot de Telegram
    try:
        # Verificar acceso a la API de Telegram
        if not check_telegram_api_access():
            logger.warning("No se pudo acceder a la API de Telegram directamente. Puede necesitar un proxy.")
        
        # Configurar el proxy si está habilitado
        request_kwargs = {
            'read_timeout': REQUEST_TIMEOUT,
            'connect_timeout': REQUEST_TIMEOUT
        }
        
        if USE_PROXY and PROXY_URL:
            logger.info(f"Utilizando proxy: {PROXY_URL}")
            proxy_auth = None
            if PROXY_USERNAME and PROXY_PASSWORD:
                proxy_auth = (PROXY_USERNAME, PROXY_PASSWORD)
                
            request_kwargs['proxy_url'] = PROXY_URL
            if proxy_auth:
                request_kwargs['urllib3_proxy_kwargs'] = {
                    'username': PROXY_USERNAME,
                    'password': PROXY_PASSWORD
                }
        
        # Crear el Request con la configuración personalizada
        request = Request(**request_kwargs)
        
        # Crear bot con el request personalizado
        bot = Bot(token=TELEGRAM_TOKEN, request=request)
        
        # Inicializar el Updater con el bot personalizado
        updater = Updater(bot=bot)
        dispatcher = updater.dispatcher
        telegram_updater = updater
        
        # Registrar handlers
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("subscribe", subscribe_command))
        dispatcher.add_handler(CommandHandler("publish", publish_command))
        dispatcher.add_handler(CommandHandler("status", status_command))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        
        # Iniciar el bot
        updater.start_polling()
        logger.info("Bot de Telegram iniciado")
        
        # Ejecutar el bot hasta que se presione Ctrl-C
        updater.idle()
        
    except Exception as e:
        logger.error(f"Error al inicializar bot de Telegram: {e}")
        logger.error("Detalles del error:", exc_info=True)
        
        # Sugerencias específicas para errores comunes
        if "timed out" in str(e).lower():
            logger.error("Sugerencia: Aumente el valor de REQUEST_TIMEOUT en el archivo .env o configure un proxy.")
        elif "proxy" in str(e).lower():
            logger.error("Sugerencia: Verifique la configuración del proxy en el archivo .env")
        elif "certificate" in str(e).lower():
            logger.error("Sugerencia: Puede haber un problema con los certificados SSL en su sistema.")
    
    finally:
        # Limpiar recursos
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
            logger.info("Conexión MQTT cerrada")

if __name__ == '__main__':
    main()
