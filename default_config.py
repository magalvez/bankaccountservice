"""
    CONFIG ENV
"""
import logging

from datetime import timedelta

SECRET_KEY = "Pl@yV0XfdsjkEERkjkW1jk$5Jk%#12dsfdsadjk32"

WTF_CSRF_ENABLED = True
CSRF_ENABLED = True

# Avoid 404 response default message
ERROR_404_HELP = False

# JWT CONSTANTS
JWT_AUTH_URL_RULE = "/service/auth"
JWT_EXPIRATION_DELTA = timedelta(days=1)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
