from __future__ import unicode_literals

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class MailItem(models.Model):
#    created = models.DateTimeField(auto_now_add=True)

    senderName = models.CharField(max_length=50, blank=True, default='')
    senderAddress = models.CharField(max_length=200, blank=True, default='')
    senderCity = models.CharField(max_length=50, blank=True, default='')
    senderState = models.CharField(max_length=20, blank=True, default='')
    senderZip = models.CharField(max_length=20, blank=True, default='')
    senderCountry = models.CharField(max_length=40, blank=True, default='')

    recipientName = models.CharField(max_length=100, blank=True, default='')
    recipientAddress = models.CharField(max_length=200, blank=True, default='')
    recipientCity = models.CharField(max_length=50, blank=True, default='')
    recipientState = models.CharField(max_length=20, blank=True, default='')
    recipientZip = models.CharField(max_length=20, blank=True, default='')
    recipientCountry = models.CharField(max_length=40, blank=True, default='')

    message = models.CharField(max_length=10000, blank=True, default='')
    status = models.CharField(max_length=20, blank=True, default='')

    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

