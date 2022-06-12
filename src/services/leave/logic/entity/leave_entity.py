from enum import Enum


class LeaveStatus(Enum):
    INITIATED = "initiated"
    DECLINE = "decline"
    CANCELED = "canceled"
    APPROVE = "approve"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def options(cls):
        return tuple(i.value for i in cls)
