import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Configuración de MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "telegram_mqtt_bot")
MQTT_TOPIC_BASE = os.getenv("MQTT_TOPIC_BASE", "telegram/mqtt")
MQTT_TOPIC_SUBSCRIBE = os.getenv("MQTT_TOPIC_SUBSCRIBE", MQTT_TOPIC_BASE + "/#")

# Temas MQTT predefinidos
TOPIC_OUTGOING = f"{MQTT_TOPIC_BASE}/outgoing"
TOPIC_INCOMING = f"{MQTT_TOPIC_BASE}/incoming"

# Configuración de conexión
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 20))
USE_PROXY = os.getenv("USE_PROXY", "False").lower() == "true"
PROXY_URL = os.getenv("PROXY_URL", "")
PROXY_USERNAME = os.getenv("PROXY_USERNAME", "")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD", "")
