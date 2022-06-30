from django.test import TestCase
from .models import Sess
# Create your tests here.

from django.contrib.sessions.models import Session
Session.objects.all().delete()