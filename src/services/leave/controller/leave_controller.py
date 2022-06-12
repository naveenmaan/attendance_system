"""
@author: Naveen Maan
@date: 2022-06-11
"""

import json
import validictory
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.custom_auth import CustomAuthentication, CustomPermission
from src.services.leave.config.leave_config import LEAVE_RAISE, TOKEN_VALIDATION
from src.services.leave.models.leave_model import Leave
from src.services.leave.logic.manager.leave_manager import LeaveManager


class LeaveController(APIView):

    """
    Endpoint to handle employee leave requests

    """

    authentication_classes = [CustomAuthentication]
    permission_classes = [CustomPermission]

    def get(self, request, *args, **kwargs):
        """
        Method to handle the leave details actions


        url: /leave/request
        url: /leave/request/{request_id}

        Args:
            request:{
                status: pending/all
            }
            *args:
            **kwargs:

        Returns:

        """

        response = {}
        response_status = None
        try:
            auth_token = request.META.get('HTTP_TOKEN')
            validictory.validate(auth_token, TOKEN_VALIDATION, disallow_unknown_properties=True, fail_fast=False)
            validictory.validate(request.data, LEAVE_RAISE['get'], disallow_unknown_properties=True, fail_fast=False)
            request_id = kwargs.get("request_id", None)
            response_status, response = LeaveManager(auth_token).get_leaves(request_id, request.data)
        except validictory.ValidationError as ex:
            response_status = status.HTTP_403_FORBIDDEN
            response = {
                "status": "failed",
                "reason": str(ex)
            }
        except Leave.DoesNotExist:
            response_status = status.HTTP_204_NO_CONTENT
            response = {
                "status": "failed",
                "reason": "Request does not exist"
            }
        except Exception as ex:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {
                "status": "failed",
                "reason": str(ex)
            }

        return Response(response, response_status)

    def post(self, request, *args, **kwargs):
        """
        Method to handle the leave creation action

        url: /leave/request
        Args:
            request: {
                from_date: 2022-03-01,
                to_date: 22-03-05,
                reason: leave
            }
            *args:
            **kwargs:

        Returns:

        """
        response = {}
        response_status = None
        try:
            auth_token = request.META.get('HTTP_TOKEN')
            validictory.validate(auth_token, TOKEN_VALIDATION, disallow_unknown_properties=True, fail_fast=False)
            validictory.validate(request.data, LEAVE_RAISE['post'], disallow_unknown_properties=True, fail_fast=False)
            response_status, response = LeaveManager(auth_token).raise_leave_request(request.data)
        except validictory.ValidationError as ex:
            response_status = status.HTTP_403_FORBIDDEN
            response = {
                "status": "failed",
                "reason": str(ex)
            }
        except Exception as ex:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {
                "status": "failed",
                "reason": str(ex)
            }

        return Response(response, response_status)

    def patch(self, request, *args, **kwargs):
        """
        Method to handle the change in leave request


        url: /leave/request/{request_id}
        Args:
            request: {
                status: canceled
                comment: test
            }
            *args:
            **kwargs:

        Returns:

        """

        response = {}
        response_status = None
        try:
            auth_token = request.META.get('HTTP_TOKEN')
            if not kwargs.get("request_id"):
                raise validictory.validator.RequiredFieldValidationError("request_id is missing")
            validictory.validate(auth_token, TOKEN_VALIDATION, disallow_unknown_properties=True, fail_fast=False)
            validictory.validate(request.data, LEAVE_RAISE['patch'], disallow_unknown_properties=True, fail_fast=False)
            response_status, response = LeaveManager(auth_token).update_leave_request_status(kwargs['request_id'], request.data)
        except validictory.ValidationError as ex:
            response_status = status.HTTP_403_FORBIDDEN
            response = {
                "status": "failed",
                "reason": str(ex)
            }
        except Leave.DoesNotExist:
            response_status = status.HTTP_204_NO_CONTENT
            response = {
                "status": "failed",
                "reason": "Request does not exist"
            }
        except Exception as ex:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {
                "status": "failed",
                "reason": str(ex)
            }

        return Response(response, response_status)


class LeaveVerifyController(APIView):

    """
    Endpoint to handle employee leave requests

    """

    authentication_classes = [CustomAuthentication]
    permission_classes = [CustomPermission]

    def get(self, request, *args, **kwargs):
        """
        Method to handle the leave details actions


        url: /leave/verify
        url: /leave/verify/{request_id}

        Args:
            request:{
                status: pending/all
            }
            *args:
            **kwargs:

        Returns:

        """

        response = {}
        response_status = None
        try:
            auth_token = request.META.get('HTTP_TOKEN')

            validictory.validate(auth_token, TOKEN_VALIDATION, disallow_unknown_properties=True, fail_fast=False)
            validictory.validate(request.data, LEAVE_RAISE['get'], disallow_unknown_properties=True, fail_fast=False)
            request_id = kwargs.get("request_id", None)
            response_status, response = LeaveManager(auth_token, admin=True).get_leaves(request_id, request.data)
        except validictory.ValidationError as ex:
            response_status = status.HTTP_403_FORBIDDEN
            response = {
                "status": "failed",
                "reason": str(ex)
            }
        except Leave.DoesNotExist:
            response_status = status.HTTP_204_NO_CONTENT
            response = {
                "status": "failed",
                "reason": "Request does not exist"
            }
        except Exception as ex:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {
                "status": "failed",
                "reason": str(ex)
            }

        return Response(response, response_status)

    def patch(self, request, *args, **kwargs):
        """
        Method to handle the change in leave request


        url: /leave/verify/{request_id}
        Args:
            request: {
                status: canceled
                comment: test
            }
            *args:
            **kwargs:

        Returns:

        """

        response = {}
        response_status = None
        try:
            auth_token = request.META.get('HTTP_TOKEN')
            validictory.validate(auth_token, TOKEN_VALIDATION, disallow_unknown_properties=True, fail_fast=False)

            if not kwargs.get("request_id"):
                raise validictory.validator.RequiredFieldValidationError("request_id is missing")

            validictory.validate(request.data, LEAVE_RAISE['verify_patch'], disallow_unknown_properties=True, fail_fast=False)
            response_status, response = LeaveManager(auth_token, admin=True).update_leave_request_status(kwargs['request_id'], request.data)
        except validictory.ValidationError as ex:
            response_status = status.HTTP_403_FORBIDDEN
            response = {
                "status": "failed",
                "reason": str(ex)
            }
        except Leave.DoesNotExist:
            response_status = status.HTTP_204_NO_CONTENT
            response = {
                "status": "failed",
                "reason": "Request does not exist"
            }
        except Exception as ex:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {
                "status": "failed",
                "reason": str(ex)
            }

        return Response(response, response_status)
