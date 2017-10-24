from django.conf import settings

import telegram


def send_log():
	"""
	"""
	bot = telegram.Bot(settings.TELEGRAM_BOT_TOKEN)
	