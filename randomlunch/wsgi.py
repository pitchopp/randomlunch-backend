import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/bitnami/apps/django/django_projects/randomlunch-backend')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/randomlunch-backend/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "randomlunch.settings")
application = get_wsgi_application()
