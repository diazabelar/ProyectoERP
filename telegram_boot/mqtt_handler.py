import paho.mqtt.client as mqtt
import logging
from typing import Callable, Any, Dict, Optional
from config import *

logger = logging.getLogger(__name__)

class MqttClient:
    def __init__(self, 
                 client_id: str,
                 on_message_callback: Callable[[str, str], None],
                 broker: str = MQTT_BROKER,
                 port: int = MQTT_PORT,
                 username: str = MQTT_USERNAME,
                 password: str = MQTT_PASSWORD,
                 topic_base: str = MQTT_TOPIC_BASE):
        """
        Inicializa un cliente MQTT
        
        :param client_id: Identificador único del cliente
        :param on_message_callback: Función a llamar cuando se recibe un mensaje
        :param broker: Dirección del broker MQTT
        :param port: Puerto del broker MQTT
        :param username: Usuario para autenticación
        :param password: Contraseña para autenticación
        :param topic_base: Tema base para las suscripciones
        """
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topic_base = topic_base
        self.client = None
        self.on_external_message = on_message_callback
        
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback interno cuando se conecta al broker MQTT"""
        if rc == 0:
            logger.info(f"Conectado al broker MQTT {self.broker}:{self.port}")
            # Suscribirse al tema base con comodín para recibir todos los mensajes
            subscription_topic = f"{self.topic_base}/#"
            client.subscribe(subscription_topic)
            logger.info(f"Suscrito a {subscription_topic}")
        else:
            logger.error(f"Error de conexión MQTT con código {rc}")
            
    def _on_message(self, client, userdata, msg):
        """Callback interno cuando se recibe un mensaje"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            logger.info(f"Mensaje MQTT recibido en {topic}: {payload}")
            
            # Llamar al callback externo con el tema y el payload
            if self.on_external_message:
                self.on_external_message(topic, payload)
                
        except Exception as e:
            logger.error(f"Error procesando mensaje MQTT: {e}")
    
    def connect(self) -> bool:
        """Conecta al broker MQTT y retorna True si tiene éxito"""
        try:
            # Usar MQTTv5 para evitar el warning de deprecación
            self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv5)
            
            # Configurar callbacks
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            
            # Configurar credenciales si están disponibles
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            
            # Conectar al broker
            self.client.connect(self.broker, self.port, 60)
            
            # Iniciar el loop en un hilo separado
            self.client.loop_start()
            return True
            
        except Exception as e:
            logger.error(f"Error al conectar con el broker MQTT: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del broker MQTT"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Desconectado del broker MQTT")
    
    def publish(self, topic: str, payload: str) -> bool:
        """Publica un mensaje en un tema y retorna True si tiene éxito"""
        if not self.client:
            logger.error("Cliente MQTT no inicializado")
            return False
            
        try:
            result = self.client.publish(topic, payload)
            if result.rc == 0:
                logger.info(f"Mensaje publicado en {topic}")
                return True
            else:
                logger.error(f"Error publicando mensaje: código {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Error al publicar mensaje: {e}")
            return False
            
    def subscribe(self, topic: str) -> bool:
        """Se suscribe a un tema adicional y retorna True si tiene éxito"""
        if not self.client:
            logger.error("Cliente MQTT no inicializado")
            return False
            
        try:
            result = self.client.subscribe(topic)
            if result[0] == 0:
                logger.info(f"Suscrito a {topic}")
                return True
            else:
                logger.error(f"Error al suscribirse a {topic}: código {result[0]}")
                return False
        except Exception as e:
            logger.error(f"Error al suscribirse: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Verifica si el cliente está conectado"""
        return self.client and self.client.is_connected()
