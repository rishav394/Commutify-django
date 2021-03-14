from functools import wraps

import bcrypt
from rest_framework import status
from rest_framework.response import Response


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())
