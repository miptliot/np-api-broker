"""Middleware classes for third_party_auth."""

from social.apps.django_app.middleware import SocialAuthExceptionMiddleware


class ExceptionMiddleware(SocialAuthExceptionMiddleware):
    pass