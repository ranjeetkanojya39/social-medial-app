"""
ASGI config for socialmedia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
=======
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
>>>>>>> 8e6df7d041b0b59b7b10caede3184c4b06cee6ff
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialmedia.settings")
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
>>>>>>> 8e6df7d041b0b59b7b10caede3184c4b06cee6ff

application = get_asgi_application()
