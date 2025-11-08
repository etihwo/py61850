from enum import Enum


class ControlModel(Enum):
    """Control model"""

    STATUS_ONLY = 0
    """No support for control functions. Control object only support
    status information."""

    DIRECT_NORMAL = 1
    """Direct control with normal security. Supports Operate,
    TimeActivatedOperate (optional), and Cancel (optional)."""

    SBO_NORMAL = 2
    """Select before operate (SBO) with normal security. Supports Select,
    Operate, TimeActivatedOperate (optional), and Cancel (optional)."""

    DIRECT_ENHANCED = 3
    """Direct control with enhanced security (enhanced security includes
    the CommandTermination service)"""

    SBO_ENHANCED = 4
    """Select before operate (SBO) with enhanced security (enhanced
    security includes the CommandTermination service)"""


class ControlAddCause(Enum):
    """Additional cause information for control model errors

    Used in LastApplError and CommandTermination messages.
    """

    UNKNOWN = 0
    NOT_SUPPORTED = 1
    BLOCKED_BY_SWITCHING_HIERARCHY = 2
    SELECT_FAILED = 3
    INVALID_POSITION = 4
    POSITION_REACHED = 5
    PARAMETER_CHANGE_IN_EXECUTION = 6
    STEP_LIMIT = 7
    BLOCKED_BY_MODE = 8
    BLOCKED_BY_PROCESS = 9
    BLOCKED_BY_INTERLOCKING = 10
    BLOCKED_BY_SYNCHROCHECK = 11
    COMMAND_ALREADY_IN_EXECUTION = 12
    BLOCKED_BY_HEALTH = 13
    ONE_OF_N_CONTROL = 14
    ABORTION_BY_CANCEL = 15
    TIME_LIMIT_OVER = 16
    ABORTION_BY_TRIP = 17
    OBJECT_NOT_SELECTED = 18
    OBJECT_ALREADY_SELECTED = 19
    NO_ACCESS_AUTHORITY = 20
    ENDED_WITH_OVERSHOOT = 21
    ABORTION_DUE_TO_DEVIATION = 22
    ABORTION_BY_COMMUNICATION_LOSS = 23
    ABORTION_BY_COMMAND = 24
    NONE = 25
    INCONSISTENT_PARAMETERS = 26
    LOCKED_BY_OTHER_CLIENT = 27


class ControlLastApplError(Enum):
    """Error type for control models

    Used in LastApplError and CommandTermination messages.
    """

    NO_ERROR = 0
    UNKNOWN = 1
    TIMEOUT_TEST = 2
    OPERATOR_TEST = 3
