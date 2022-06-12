import validictory
from rest_framework import authentication, permissions
from rest_framework import exceptions

from core.permission_confg import TOKEN_VALIDATION, PERMISSION_NAME_MAPPING
from src.models.auth_token_model import AuthToken


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.META.get('HTTP_TOKEN')

        validictory.validate(auth_token, TOKEN_VALIDATION, disallow_unknown_properties=True, fail_fast=False)

        try:
            user = AuthToken.objects.get(auth_token=auth_token)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)


class CustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        permission_name = PERMISSION_NAME_MAPPING.get(type(view).__name__)

        auth_token = request.META.get('HTTP_TOKEN')
        user = AuthToken.objects.get(auth_token=auth_token)
        # Instance must have an attribute named `owner`.
        return user.user.has_perm(permission_name)