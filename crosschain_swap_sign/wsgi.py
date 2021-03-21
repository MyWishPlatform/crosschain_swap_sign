import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crosschain_swap_sign.settings')

application = get_wsgi_application()
