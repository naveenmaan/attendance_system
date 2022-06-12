"""
@author: Naveen Maan
@date: 2022-06-11
"""


from rest_framework import serializers
from src.services.leave.models.leave_model import Leave


class LeaveSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Leave
        fields = ["id", "username", "from_date", "to_date", "status", "reason", "created_datetime"]


class LeaveModifiedSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Leave
        fields = ["id", "username", "from_date", "to_date", "status", "reason", "comment", "created_datetime", "modified_datetime"]


class LeaveSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Leave
        fields = ["id", "username", "from_date", "to_date", "status", "reason", "comment", "created_datetime", "created_by", "modified_datetime", "modified_by"]
