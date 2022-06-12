"""
@author: Naveen Maan
@date: 2022-06-11
"""

from django.conf.urls import url
from django.urls import path, include
from src.services.leave.controller.leave_controller import LeaveController, LeaveVerifyController

urlpatterns = [
    path('leave/request', LeaveController.as_view(), name="request"),
    path('leave/request/<int:request_id>', LeaveController.as_view(), name="request"),

    path('leave/verify', LeaveVerifyController.as_view(), name="verify"),
    path('leave/verify/<int:request_id>', LeaveVerifyController.as_view(), name="verify"),
]