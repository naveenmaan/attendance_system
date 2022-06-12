from django.contrib import admin

from .models.auth_token_model import AuthToken


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ("auth_token", "get_user_name")