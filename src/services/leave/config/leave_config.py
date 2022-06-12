from src.services.leave.logic.entity.leave_entity import LeaveStatus

TOKEN_VALIDATION = {
    "type": "string",
    "pattern": r"[a-zA-z0-9-]+"
}

LEAVE_RAISE = {
    "get": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": LeaveStatus.options(),
                "required": False
            },
            "limit": {
                "type": "integer",
                "required": False
            },
            "skip": {
                "type": "integer",
                "required": False
            }
        }
    },
    "post": {
        "type": "object",
        "properties": {
            "from_date": {
                "type": "string", "pattern": r"\d{4}-\d\d-\d{2}"
            },
            "to_date": {
                "type": "string", "pattern": r"\d{4}-\d\d-\d{2}"
            },
            "reason": {
                "type": "string",
                "minLength": 1,
                "maxLength": 255,
                "regex": r"[a-zA-z.0-9 ]+"
            },
        }
    },
    "patch": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": [LeaveStatus.CANCELED.value]
            },
            "comment": {
                "type": "string",
                "minLength": 1,
                "maxLength": 255,
                "regex": r"[a-zA-z.0-9 ]+"
            }
        }
    },
    "verify_patch": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": [LeaveStatus.APPROVE.value, LeaveStatus.DECLINE.value]
            },
            "comment": {
                "type": "string",
                "minLength": 1,
                "maxLength": 255,
                "regex": r"[a-zA-z.0-9 ]+"
            }
        }
    }
}