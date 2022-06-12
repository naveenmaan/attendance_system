"""
@author: Naveen Maan
@date: 2022-06-11
"""

import datetime
from rest_framework import status

from core.custom_exception import WrongDateRangeError, DuplicateRequestError, InvalidRequestError
from src.services.leave.logic.entity.leave_entity import LeaveStatus
from src.services.leave.serializers.leave_serilizer import LeaveSerializer, LeaveSearchSerializer, LeaveModifiedSerializer

from src.models.auth_token_model import AuthToken
from src.services.leave.models.leave_model import Leave

from src.services.leave.logic.utility.format_response import format_response

class LeaveManager(object):
    """
    Manager class to handle all the leave actions
    """

    def __init__(self, auth_token, admin=False):
        """
        method to init the required resources
        Args:
            auth_token: auth token for the user
            admin: is admin browsing
        """

        self.auth_token = auth_token
        self.user = AuthToken.objects.get(auth_token=auth_token)
        self.admin = admin

    def __get_leaves_by_request_id(self, request_id, request, serialize=True):
        """
        method to get the leaves requests
        Args:
            request: {
                "id": 14,
                "username": "user1",
                "from_date": "2022-06-14",
                "to_date": "2022-06-14",
                "status": "canceled",
                "reason": "Leave",
                "created_datetime": "2022-06-12T08:16:08.711411Z"
            }
            request_id: 1

        Returns:
            {
                request: [],
                total_page: 10,
                hast_previous_page: true,
                hast_next_page: true,
            }

        """

        leave_object = Leave.objects.filter(id=request_id)

        if not self.admin:
            leave_object = leave_object.filter(user_id=self.user.id)
        if request:
            leave_object = leave_object.get(**request)

        if len(leave_object) == 0:
            return {}

        if not serialize:
            return leave_object

        return LeaveSearchSerializer(leave_object[0]).data

    def __get_leave_requests(self, request):
        """
        method to get the leaves requests
        Args:
            request: {
                username: test,
                status: initiated,
                skip: 10,
                limit: 10
            }
            request_id: 1

        Returns:
            [
                {
                    "id": 14,
                    "username": "user1",
                    "from_date": "2022-06-14",
                    "to_date": "2022-06-14",
                    "status": "canceled",
                    "reason": "Leave",
                    "created_datetime": "2022-06-12T08:16:08.711411Z"
                }
            ]
        """

        if not self.admin:
            request['user_id'] = self.user.id
        leave_object = Leave.objects.filter(**request)

        return LeaveSearchSerializer(leave_object, many=True).data

    def get_leaves(self, request_id, request):
        """
        method to get the leaves requests
        Args:
            request: {
                username: test,
                status: initiated,
                skip: 10,
                limit: 10
            }
            request_id: 1

        Returns:
            {
                data: [],
                total_page: 10,
                has_previous_page: true,
                has_next_page: true,
            }

        """

        try:
            leave_object = None
            result = {}
            if request_id:
                result = self.__get_leaves_by_request_id(request_id, request)
            else:
                result = self.__get_leave_requests(request)

            # format the search
            result = format_response(result, request)

            return status.HTTP_200_OK, result

        except Exception as ex:
            raise ex

    def __leave_request_validation(self, request):
        """
        Method to validate the leave request
        Args:
            request: {
                "from_date": 2022-02-02,
                "to_date" : 2022-02-03,
                "reason": test
            }

        Returns:

        """

        # validate the from_date and to_date

        from_date = datetime.datetime.strptime(request['from_date'], "%Y-%m-%d")
        to_date = datetime.datetime.strptime(request['to_date'], "%Y-%m-%d")

        if from_date > to_date:
            raise WrongDateRangeError

    def __is_already_raised(self, request):
        """
        Method to check if the same leave request is raised
        Args:
            request: {
                "from_date": 2022-02-02,
                "to_date" : 2022-02-03,
                "reason": test
            }

        Returns:

        """

        result = Leave.objects.filter(from_date__range=[request['from_date'], request['to_date']],
                                      status__in=[LeaveStatus.INITIATED, LeaveStatus.APPROVE])

        if len(result):
            raise DuplicateRequestError

    def raise_leave_request(self, request):
        """
        method to raise the leave request
        Args:
            request: {
                "from_date" : 2022-02-03,
                "to_date": 2022-02-05,
                "reason": leave
            }

        Returns: {
            id: 5,
            username: test
            "from_date" : 2022-02-03,
            "to_date": 2022-02-05,
            "reason": leave,
            "status": initiated,
            "created_datetime": now(),
            "modified_datetime": none,
            "modified_by": none
        }

        """

         # validate the leave request
        self.__leave_request_validation(request)
        self.__is_already_raised(request)

        # create the leave request
        leave_mode_object = Leave(**request)
        leave_mode_object.user = self.user.user
        leave_mode_object.save()
        leave_mode_object.created_by = self.user.user
        leave_mode_object = LeaveSerializer(leave_mode_object, many=False)

        return status.HTTP_201_CREATED, leave_mode_object.data

    def update_leave_request_status(self, request_id, request):
        """
        method to change the status of the
        Args:
            request_id: 12,
            request: {
                "status": cancel,
                "comment" : test
            }

        Returns: {
            id: 5,
            username: test
            "from_date" : 2022-02-03,
            "to_date": 2022-02-05,
            "reason": leave,
            "status": initiated,
            "created_datetime": now(),
            "modified_datetime": now()
        }

        """

        # check is request valid

        try:
            leave_result = self.__get_leaves_by_request_id(request_id, {}, serialize=False)

            if leave_result == {}:
                raise Leave.DoesNotExist

            leave_result = leave_result[0]

            if leave_result.status != LeaveStatus.INITIATED.value:
                raise InvalidRequestError

            leave_result.status=request['status']
            leave_result.comment=request['comment']
            leave_result.modified_datetime = datetime.datetime.now()
            leave_result.modified_by = self.user.user.username
            leave_result.save()

            return status.HTTP_200_OK, LeaveModifiedSerializer(leave_result).data
        except Exception as ex:
            raise ex