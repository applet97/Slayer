# -*- coding: utf-8 -*-
from django.conf import settings
import celery
import urllib
import urllib2

from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.conf import settings
#from api.models import BlackList


@celery.task(default_retry_delay=2 * 60, max_retries=2)  # retry in 2 minutes
def email(to, subject, message):
    """
    Sends email to user/users. 'to' parameter must be a string or list
    """
    # Convert to list if one user's email is passed
    if isinstance(to, basestring):  # Python 2.x only
        to = [to]
    if isinstance(to, set):  # Python 2.x only
        to = list(to)
    try:
        msg = EmailMessage(subject, message, from_email=settings.FROM_EMAIL, to=to)
        msg.content_subtype = "html"
        msg.send()
    except Exception, exc:
        raise email.retry(exc=exc)