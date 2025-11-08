"""Implements function and class relative to control on client side"""

import ctypes
import datetime
from collections.abc import Callable
from ctypes import byref, c_bool, c_int, c_void_p
from enum import Enum, Flag
from typing import TYPE_CHECKING

from ..binding.iec61850.client import CommandTerminationHandler
from ..binding.loader import Wrapper
from ..common import (
    ACSIClass,
    ControlAddCause,
    ControlLastApplError,
    ControlModel,
    MmsType,
    MmsValue,
    OrCat,
    Quality,
    Timestamp,
)
from ..helper import convert_to_bytes, convert_to_datetime
from .enums import IedClientError
from .errors import LastApplError

if TYPE_CHECKING:
    from .connection import IedConnection


class ControlActionType(Enum):
    """Cause of the ControlObjectClient_ControlActionHandler invocation"""

    SELECT = 0
    """callback was invoked because of a select command"""
    OPERATE = 1
    """callback was invoked because of an operate command"""
    CANCEL = 2
    """callback was invoked because of a cancel command"""


class ControlObject:
    """client control object

    It is used to handle all client side functions of a controllable data object.
    """

    def __init__(self, handle: c_void_p) -> None:
        self._handle = handle
        self._termination_handler = None

    def __del__(self):
        Wrapper.lib.ControlObjectClient_destroy(self._handle)

    @property
    def object_reference(self) -> bytes:
        """Object reference of the control data object."""
        return Wrapper.lib.ControlObjectClient_getObjectReference(self._handle)

    @property
    def control_model(self) -> ControlModel:
        """Current control model (local representation) applied to the control object."""
        value = Wrapper.lib.ControlObjectClient_getControlModel(self._handle)
        return ControlModel(value)

    @property
    def ctl_val_type(self) -> MmsType:
        """Return the type of ctlVal."""
        value = Wrapper.lib.ControlObjectClient_getCtlValType(self._handle)
        return MmsType(value)

    def get_last_error(self) -> "IedClientError":
        """Get the error code of the last synchronous control action
        (operate, select, select-with-value, cancel)

        Returns
        -------
        IedClientError
            Client error code
        """
        value = Wrapper.lib.ControlObjectClient_getLastError(self._handle)
        return IedClientError(value)

    def operate(self, ctl_val: MmsValue, oper_time: int = 0) -> bool:
        """Send an operate command to the server.

        Parameters
        ----------
        ctl_val : MmsValue
            Control value (for APC the value may be either AnalogueValue
            (MMS_STRUCT) or MMS_FLOAT/MMS_INTEGER
        oper_time : int, optional
            Time when the command has to be executed (for time activated
            control), by default 0. The value represents the local time
            of the server in milliseconds since epoch. If this value is
            0 the command will be executed instantly


        Returns
        -------
        bool
            True if operation has been successful, False otherwise.
        """

        return Wrapper.lib.ControlObjectClient_operate(self._handle, ctl_val.handle, oper_time)

    def select(self) -> bool:
        """Send a select command to the server.

        The select command is only used for the control model
        "select-before-operate with normal security"(SBO_NORMAL). The
        select command has to be sent before the operate command can be
        used.

        Returns
        -------
        bool
            True if operation has been successful, False otherwise.
        """
        return Wrapper.lib.ControlObjectClient_select(self._handle)

    def select_with_value(self, ctl_val: MmsValue) -> bool:
        """Send an select with value command to the server.

        The select-with-value command is only used for the control model
        "select-before-operate with enhanced security" (SBO_ENHANCED).
        The select-with-value command has to be sent before the operate
        command can be used.

        Parameters
        ----------
        ctl_val : MmsValue
            Control value (for APC the value may be either AnalogueValue
            (MMS_STRUCT) or MMS_FLOAT/MMS_INTEGER

        Returns
        -------
        bool
            True if operation has been successful, False otherwise.
        """
        return Wrapper.lib.ControlObjectClient_selectWithValue(self._handle, ctl_val.handle)

    def cancel(self) -> bool:
        """Send a cancel command to the server.

        The cancel command can be used to stop an ongoing operation (when
        the server and application support this) and to cancel a former
        select command.

        Returns
        -------
        bool
            True if operation has been successful, False otherwise.
        """
        return Wrapper.lib.ControlObjectClient_cancel(self._handle)

    # def ControlObjectClient_operateAsync(self)->int:
    #     return Wrapper.lib.ControlObjectClient_operateAsync.argtypes = [
    #         self._handle,
    #         POINTER(IedClientError),  # IedClientError* err,
    #         POINTER(MmsValue),  # MmsValue* ctlVal,
    #         c_uint64,  # uint64_t operTime
    #         ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler,
    #         c_void_p,  # void* parameter
    #     ]

    # def ControlObjectClient_selectAsync(self)->int:
    #     return Wrapper.lib.ControlObjectClient_selectAsync.argtypes = [
    #         self._handle,
    #         POINTER(IedClientError),  # IedClientError* err,
    #         ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler,
    #         c_void_p,  # void* parameter
    #     ]

    # def ControlObjectClient_selectWithValueAsync(self)->int:
    #     return Wrapper.lib.ControlObjectClient_selectWithValueAsync.argtypes = [
    #         self._handle,
    #         POINTER(IedClientError),  # IedClientError* err
    #         POINTER(MmsValue),  # MmsValue* ctlVal
    #         ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler
    #         c_void_p,  #  void* parameter
    #     ]

    # def ControlObjectClient_cancelAsync(self):
    #     Wrapper.lib.ControlObjectClient_cancelAsync.argtypes = [
    #         self._handle,
    #         POINTER(IedClientError),  # IedClientError* err
    #         ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler
    #         c_void_p,  #  void* parameter
    #     ]
    #     lib.ControlObjectClient_cancelAsync.restype = c_uint32

    def get_last_appl_error(self) -> "LastApplError":
        """Get the last received control application error

        Returns
        -------
        LastApplError
            Control application error
        """
        value = Wrapper.lib.ControlObjectClient_getLastApplError(self._handle)
        return LastApplError(value)

    def set_test_mode(self, value: bool):
        """Set the test mode

        When the server supports test mode the commands that are sent with
        the test flag set are not executed (will have no effect on the
        ttached physical process).

        Parameters
        ----------
        value : bool
            Value of the test flag
        """
        Wrapper.lib.ControlObjectClient_setTestMode(self._handle, value)

    def set_origin(self, or_ident: str | bytes, or_cat: OrCat):
        """Set the origin parameter for control commands.

        The origin parameter is used to identify the client/application
        that sent a control command. It is intended for later analysis.

        Parameters
        ----------
        or_ident : str | bytes
            Originator identification
        or_cat : OrCat
            Originator category
        """
        or_ident = convert_to_bytes(or_ident)
        Wrapper.lib.ControlObjectClient_setOrigin(self._handle, or_ident, or_cat.value)

    def use_constant_t(self, use_constant_t: bool):
        """Use a constant T parameter for all command (select, operate, cancel) of a single control sequence.

        Parameters
        ----------
        use_constant_t : bool
            Enable this behavior with true, disable with false
        """
        Wrapper.lib.ControlObjectClient_useConstantT(self._handle, use_constant_t)

    def set_interlock_check(self, value: bool):
        """Set the value of the interlock check flag when a control command is sent.

        Parameters
        ----------
        value : bool
            If true the server will perform a interlock check if supported
        """
        Wrapper.lib.ControlObjectClient_setInterlockCheck(self._handle, value)

    def set_synchro_check(self, value: bool):
        """Set the value of the synchro check flag when a control command is sent.

        Parameters
        ----------
        value : bool
            If true the server will perform a synchro check if supported
        """
        Wrapper.lib.ControlObjectClient_setSynchroCheck(self._handle, value)

    def on_termination(self, callback: Callable[["ControlObject"], None]):
        """Set the command termination callback handler for this control object.

        This callback is invoked whenever a CommandTermination+ or
        CommandTermination- message is received. To distinguish between a
        CommandTermination+ and CommandTermination- please use the
        ``get_last_appl_error`` function. In case of CommandTermination+
        the return value of ``get_last_appl_error`` has error=NO_ERROR
        and ``add_cause``=UNKNOWN set. When ``add_cause`` is different
        from UNKNOWN then the client received a CommandTermination-
        message.

        Parameters
        ----------
        callback : Callable[[&quot;ControlObject&quot;], None]
            Callback function to be used
        """

        def fun(parameter: int | None, control_client: c_void_p):
            callback(self)

        handler = CommandTerminationHandler(fun)
        Wrapper.lib.ControlObjectClient_setCommandTerminationHandler(self._handle, handler, None)
        self._termination_handler = handler
