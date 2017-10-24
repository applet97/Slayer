import re

def get_url(url):
	a = url.split('resized/80/')
	return a[0] + a[1]