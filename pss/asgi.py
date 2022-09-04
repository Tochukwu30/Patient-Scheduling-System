"""
ASGI config for pss project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django


from pss.wsgi import *
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns
from .channelsmiddleware import TokenAuthMiddleware, TokenAuthMiddlewareStack

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pss.settings")
# django.setup()
django_asgi_app = get_asgi_application()

# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # "http": get_asgi_application(),
        "websocket": TokenAuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns,
            )
        ),
    }
)
