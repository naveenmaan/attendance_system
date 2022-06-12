"""
@author: Naveen Maan
@date: 2022-06-11
"""

from django.contrib.auth.models import User
from django.db import models

from src.services.leave.logic.entity.leave_entity import LeaveStatus


class Leave(models.Model):
    """
    models to store the leave details
    """

    class Meta:
        permissions = [
            ("request", "Can raise the leave request"),
            ("verify", "Can approve the leave request"),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=500)
    status = models.CharField(max_length=255, choices=LeaveStatus.choices(), default=LeaveStatus.INITIATED.value)
    comment = models.CharField(max_length=500, default=None, null=True)
    is_valid = models.IntegerField(default=1)
    created_by = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=255)
    modified_datetime = models.DateTimeField(auto_now=True)
