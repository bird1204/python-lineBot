#  python manage.py runserver

from django.db import models
from django.core.exceptions import ValidationError

# from skyscanner.skyscanner import Flights
# flights_service = Flights('<Your API Key>')


def validate_dialog_source(source):
  if source in ['system', 'line']:
      raise ValidationError (
        _('%(source)s is not an avaliable inputs'),
        params={'value': value},
      )

# Create your models here.
class Bot(models.Model):
  source_id = models.CharField(max_length=255)
  source_type = models.CharField(blank=False, max_length=15)
  user_name = models.CharField(max_length=255)
  status = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

class Dialog(models.Model):
  bot_id = models.IntegerField(blank=False)
  message_id = models.CharField(max_length=255)
  source = models.CharField(max_length=10, validators=[validate_dialog_source])
  content = models.TextField(default='')
  response_params = models.TextField(default='{}')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

# class Flight(models.Model):
#   country = models.CharField(max_length=5)
#   currency = models.CharField(max_length=3)
#   locale = models.CharField(max_length=10)
#   originplace = models.CharField(max_length=10)
#   destinationplace = models.CharField(max_length=10)
#   outbounddate = models.DateField(auto_now_add=True)
#   inbounddate = models.DateField(auto_now_add=True)
#   adults = models.IntegerField(default=1)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now_add=True)