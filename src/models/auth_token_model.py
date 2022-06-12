"""
@author: Naveen Maan
@date: 2022-06-11
"""

import uuid
from django.contrib.auth.models import User
from django.db import models


class AuthToken(models.Model):
    """
    Model class for auth token
    """

    auth_token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_user_name(self):
        return self.user.username
