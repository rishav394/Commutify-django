from functools import wraps

import bcrypt
from rest_framework import status
from rest_framework.response import Response

from .models import User


def valid_session(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        id = request.session.get("id", None)
        if id is not None:
            user = User.objects.filter(id=id, active=True).first()
            if user is not None:
                request.user = user
                return function(request, *args, **kwargs)
            else:
                del request.session["id"]
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    return wrap
