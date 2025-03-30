import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden

# Intentar cargar variables de entorno con dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv no está instalado. Las variables de entorno deberán configurarse manualmente o instalar el paquete con 'pip install python-dotenv'")
    # Continuar sin dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Cargar la SECRET_KEY de la variable de entorno; si no está definida, lanzar un error para evitar exponer una clave débil
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("La variable de entorno SECRET_KEY no está definida. Configure una clave secreta fuerte.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if ALLOWED_HOSTS == ['']:
    ALLOWED_HOSTS = []

# Special setting for allowing demo access without login
ALLOW_DEMO_ACCESS = True  # Can be toggled based on environment

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'simple_history',
    'import_export',
    'accounts',
    
    # Módulos del ERP
    'compras',
    'ventas',
    'productos',
    'contabilidad',
    'agenda',
    'calendario',
    'calculadora',
    'hoja_calculo',
    'notas',
    'core',  # Add the 'core' app
    'billing', # Add the 'billing' app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.GuestAccessMiddleware',    # Place right after AuthenticationMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'core.middleware.ActiveCompanyMiddleware',  # Keep this as is
]

# Add our authentication backend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
    'core.auth_backend.GuestBackend',             # Our guest backend
]

ROOT_URLCONF = 'proyecto_erp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # This line ensures Django finds your templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto_erp.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'proyectoERP'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),  # Volvemos a localhost o el valor en variable de entorno
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'connect_timeout': 30,  # Mantener tiempo de espera aumentado
            'use_unicode': True,
            # Configuración del socket - dejar que MySQL elija automáticamente
            # 'unix_socket': '',  # Comentamos esta línea para usar el socket predeterminado
        },
    }
}

print("Usando MySQL como base de datos predeterminada")

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'


