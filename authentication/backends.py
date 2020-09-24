from django.contrib.auth.models import User
import jwt

from rest_framework import authentication
from rest_framework import exceptions
from contactapi.env import JWT_SECRET_KEY

class JWTAuthentication(authentication.BaseAuthentication):


    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY)
            user = User.objects.get(username=payload['username'])
            return (user, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid.')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired, Login.')

        return super().authenticate(request)