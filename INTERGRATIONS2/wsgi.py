"""
WSGI config for INTERGRATIONS2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
from dotenv import load_dotenv
import os
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path) 
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INTERGRATIONS2.settings')

application = get_wsgi_application()

