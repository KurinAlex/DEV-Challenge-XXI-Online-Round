"""
ASGI config for application.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apiproject.settings')

application = get_asgi_application()
