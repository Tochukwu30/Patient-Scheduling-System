from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken

from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack


# @database_sync_to_async
# def get_user(token_key):
#     try:
#         return Token.objects.get(key=token_key).user
#     except Token.DoesNotExist:
#         return AnonymousUser()


@database_sync_to_async
def get_user(id):
    try:
        return get_user_model().objects.get(id=id)
    except get_user_model().DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):

        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        headers = dict(self.scope["headers"])
        if b"authorization" in headers:
            token_name, token_key = headers[b"authorization"].decode().split()
            if token_name == "Bearer":
                try:
                    # This will automatically validate the token and raise an error if token is invalid
                    UntypedToken(token_key)
                except (InvalidToken, TokenError) as e:
                    # Token is invalid
                    print(e)
                    return None
                else:
                    #  Then token is valid, decode it
                    decoded_data = jwt_decode(
                        token_key, settings.SECRET_KEY, algorithms=["HS256"]
                    )
                    # print("mwd", await get_user(id=26))
                    # print(decoded_data["user_id"])
                    user = await get_user(id=decoded_data["user_id"])
                    # print(user)
                    self.scope["user"] = await get_user(id=decoded_data["user_id"])

        # Get the token
        # token = dict(self.scope["headers"])[b"authorization"][7:]
        # print(token)

        # Try to authenticate the user

        # Return the inner application directly and let it run everything else
        # inner = self.inner(dict(self.scope, user=user))
        # return await inner(receive, send)
        inner = self.inner(self.scope, receive, send)
        return await inner


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
