from ..binding.iec61850.client import LastApplError as _cLastApplError
from ..common import ControlAddCause, ControlLastApplError


class LastApplError:
    """Detailed description of the last application error of the client connection instance"""

    def __init__(self, value: _cLastApplError) -> None:
        # Use this trick to have no limitataion on property name
        self._ctl_num = value.ctlNum
        self._error = ControlLastApplError(value.error)
        self._add_cause = ControlAddCause(value.addCause)

    @property
    def ctl_num(self) -> int:
        """Control Number, numeric identifier for the control request and can be used by the client to distinguish between the different control requests"""
        return self._ctl_num

    @property
    def error(self) -> ControlLastApplError:
        return self._error

    @property
    def add_cause(self) -> ControlAddCause:
        return self._add_cause
