"""
WSGI config for application.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apiproject.settings')

application = get_wsgi_application()
