import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django.conf import settings

from blacknoise import BlackNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ot_1018_3_0030.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
})

application = BlackNoise(application)
application.add(settings.STATIC_ROOT, "/static")
