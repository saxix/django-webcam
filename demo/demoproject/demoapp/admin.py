from django.contrib.admin import site
from demoproject.demoapp.models import DemoModel


site.register(DemoModel)
