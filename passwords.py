# Python password generator

import string
import random


def passwordgen():

	characterList = string.ascii_letters + string.digits + string.punctuation

	password = []

	for i in range(12):
		randomchar = random.choice(characterList)
		password.append(randomchar)

	password = "".join(password)

	return password

password = passwordgen()

print(password)