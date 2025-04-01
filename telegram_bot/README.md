# Bot de Telegram para MQTT

Un bot de Telegram escrito en Python que puede enviar y recibir mensajes MQTT, permitiendo integrar sistemas de IoT con la plataforma de mensajería.

## Requisitos

- Python 3.7+
- Cuenta de Telegram
- Servidor MQTT (por ejemplo, Mosquitto)

## Configuración

1. **Crear un bot en Telegram**:
   - Habla con [@BotFather](https://t.me/BotFather) en Telegram
   - Usa el comando `/newbot` y sigue las instrucciones
   - Guarda el token que te proporciona BotFather

2. **Preparar el entorno**:
   ```bash
   # Clonar o crear el directorio del proyecto
   cd /home/abe/Escritorio/telegram_boot

   # Crear entorno virtual (opcional pero recomendado)
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

   # Instalar dependencias
      python-telegram-bot==13.15
   paho-mqtt==2.1.0
   # ...existing code...
   ```

3. **Configurar variables de entorno**:
   - Edita el archivo `.env` con tu información
   - Añade el token de tu bot de Telegram
   - Configura los detalles de conexión MQTT
   - Para encontrar tu ADMIN_CHAT_ID, inicia el bot e imprime `update.effective_chat.id`

## Uso

1. **Iniciar el bot**:
   ```bash
   python main.py
   ```

2. **Comandos disponibles**:
   - `/start` - Iniciar la conversación con el bot
   - `/help` - Mostrar la ayuda con los comandos disponibles
   - `/subscribe tema` - Suscribirse a un tema MQTT específico
   - `/publish tema mensaje` - Publicar un mensaje en un tema MQTT
   - `/status` - Ver el estado de la conexión MQTT

3. **Integración con MQTT**:
   - Los mensajes enviados al bot se publican en `telegram/mqtt/outgoing`
   - Los mensajes recibidos en `telegram/mqtt/incoming` se envían al chat configurado

## Estructura de mensajes MQTT

### Para enviar un mensaje a Telegram desde MQTT:

Publica un mensaje JSON en `telegram/mqtt/incoming` con el siguiente formato:
```json
{
  "chat_id": "ID_DEL_CHAT",
  "message": "Tu mensaje aquí"
}
```

### Mensajes enviados desde Telegram a MQTT:

Se publican en `telegram/mqtt/outgoing` con el siguiente formato:
```json
{
  "chat_id": 123456789,
  "user_id": 123456789,
  "username": "usuario",
  "first_name": "Nombre",
  "message": "Contenido del mensaje",
  "timestamp": 1634567890.123
}
```

## Solución de problemas

- **Error de conexión MQTT**: Verifica que el broker MQTT esté funcionando y sea accesible
- **Bot no responde**: Comprueba que el token de Telegram sea válido y que el bot esté en ejecución
- **No llegan mensajes MQTT**: Verifica los temas de suscripción y permisos en el broker
