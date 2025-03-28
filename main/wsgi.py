import os
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

try:
    application = get_wsgi_application()
except Exception:
    traceback.print_exc()