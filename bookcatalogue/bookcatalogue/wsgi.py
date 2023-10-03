"""
WSGI config for bookcatalogue project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application

import os
import certifi

os.environ['SSL_CERT_FILE'] = certifi.where()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookcatalogue.settings')

application = get_wsgi_application()
