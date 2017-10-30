import random

def get_random_string(length=6):
	"""
	"""
	number = '023456789'
	alpha = 'abcdefghijkmnopqrstuvwxyz'
	ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	res = ''

	for i in range(length):
		which = random.randint(0, 2)
		if which is 0:
			res += random.choice(number)
		elif which is 1:
			res += random.choice(alpha)
		else:
			res += random.choice(ALPHA)

	return res