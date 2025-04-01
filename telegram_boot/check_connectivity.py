#!/usr/bin/env python3
import socket
import urllib.request
import urllib.error
import requests
import logging
import sys
from config import *

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def check_internet_connection():
    """Verifica si hay conexión a Internet"""
    try:
        # Intentar conectar a Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        logger.info("✅ Conexión básica a Internet: FUNCIONANDO")
        return True
    except OSError as e:
        logger.error(f"❌ Error al conectar con Google DNS: {e}")
    
    try:
        # Intentar con la API de Google como alternativa
        urllib.request.urlopen("https://www.google.com", timeout=5)
        logger.info("✅ Conexión a Google: FUNCIONANDO")
        return True
    except urllib.error.URLError as e:
        logger.error(f"❌ Error al conectar con Google: {e}")
    
    logger.error("❌ No se detectó conexión a Internet")
    return False

def check_telegram_api():
    """Verifica si la API de Telegram está accesible"""
    logger.info("Probando conexión a la API de Telegram...")
    
    try:
        # Verificar si podemos acceder a la API de Telegram
        response = requests.get("https://api.telegram.org", timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            logger.info("✅ API de Telegram: ACCESIBLE")
            return True
        else:
            logger.error(f"❌ API de Telegram devuelve código: {response.status_code}")
            return False
    except requests.RequestException as e:
        logger.error(f"❌ Error al conectar con la API de Telegram: {e}")
        return False

def check_telegram_bot():
    """Verifica si el bot de Telegram está configurado correctamente"""
    if not TELEGRAM_TOKEN:
        logger.error("❌ Token de Telegram no configurado en .env")
        return False
    
    try:
        # Comprobar si el token es válido
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
        
        # Configurar proxy si es necesario
        proxies = None
        if USE_PROXY and PROXY_URL:
            proxies = {
                'http': PROXY_URL,
                'https': PROXY_URL
            }
            auth = None
            if PROXY_USERNAME and PROXY_PASSWORD:
                auth = requests.auth.HTTPProxyAuth(PROXY_USERNAME, PROXY_PASSWORD)
        
        # Hacer la solicitud con o sin proxy
        response = requests.get(
            url, 
            timeout=REQUEST_TIMEOUT,
            proxies=proxies,
        )
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                logger.info(f"✅ Bot de Telegram '{bot_info['result']['username']}': VALIDADO")
                return True
        
        logger.error(f"❌ Bot de Telegram no válido: {response.text}")
        return False
    
    except requests.RequestException as e:
        logger.error(f"❌ Error al validar el bot de Telegram: {e}")
        return False

def check_mqtt_connection():
    """Verifica si el broker MQTT está accesible"""
    try:
        logger.info(f"Probando conexión MQTT a {MQTT_BROKER}:{MQTT_PORT}...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((MQTT_BROKER, MQTT_PORT))
        s.close()
        logger.info(f"✅ Broker MQTT {MQTT_BROKER}:{MQTT_PORT}: ACCESIBLE")
        return True
    except Exception as e:
        logger.error(f"❌ Error al conectar con el broker MQTT {MQTT_BROKER}:{MQTT_PORT}: {e}")
        return False

if __name__ == "__main__":
    logger.info("=== DIAGNÓSTICO DE CONECTIVIDAD ===")
    
    internet_ok = check_internet_connection()
    
    if internet_ok:
        telegram_api_ok = check_telegram_api()
        if telegram_api_ok:
            check_telegram_bot()
    
    mqtt_ok = check_mqtt_connection()
    
    logger.info("=== RESUMEN DE DIAGNÓSTICO ===")
    logger.info(f"Conexión a Internet: {'✅ OK' if internet_ok else '❌ FALLO'}")
    if internet_ok:
        logger.info(f"API de Telegram: {'✅ OK' if telegram_api_ok else '❌ FALLO'}")
    logger.info(f"Broker MQTT: {'✅ OK' if mqtt_ok else '❌ FALLO'}")
    
    if not internet_ok:
        logger.info("\nSUGERENCIA: Verifique su conexión a Internet")
    
    if internet_ok and not telegram_api_ok:
        logger.info("\nSUGERENCIA: Es posible que necesite configurar un proxy para acceder a la API de Telegram")
        logger.info("  1. Configure USE_PROXY=True en .env")
        logger.info("  2. Añada su URL de proxy en PROXY_URL en .env")
        logger.info("  3. Si el proxy requiere autenticación, añada las credenciales en PROXY_USERNAME y PROXY_PASSWORD")
    
    if not mqtt_ok:
        logger.info("\nSUGERENCIA: Verifique que el broker MQTT esté activo y que los datos de conexión sean correctos")
