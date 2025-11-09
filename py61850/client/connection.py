"""Represent function on client side"""

import ctypes
from collections.abc import Callable
from ctypes import byref, c_bool
from typing import TYPE_CHECKING

from ..binding.iec61850.client import IedClientError as _cIedClientError
from ..binding.iec61850.client import (
    IedClientGetFileHandler,
    IedConnection_ClosedHandler,
    IedConnection_StateChangedHandler,
    ReportCallbackFunction,
)
from ..binding.iec61850.client import sClientGooseControlBlock as _sClientGooseControlBlock
from ..binding.iec61850.client import sClientReportControlBlock as _sClientReportControlBlock
from ..binding.loader import Wrapper
from ..common import (
    ACSIClass,
    ControlAddCause,
    ControlLastApplError,
    FunctionalConstraint,
    LinkedList,
    MmsValue,
    Quality,
    ReportOptions,
    ReportTriggerOptions,
    Timestamp,
)
from ..helper import convert_to_bytes
from .control import ControlObject
from .dataset import DataSet
from .enums import IedClientError, IedConnectionState
from .errors import LastApplError
from .file import FileDirectoryEntry
from .goose import GooseControlBlock
from .report import Report, ReportControlBlock

if TYPE_CHECKING:
    GooseControlBlockPointer = ctypes._Pointer[_sClientGooseControlBlock]  # type: ignore
    ReportControlBlockPointer = ctypes._Pointer[_sClientReportControlBlock]  # type: ignore
else:
    GooseControlBlockPointer = ctypes.POINTER(_sClientGooseControlBlock)
    ReportControlBlockPointer = ctypes.POINTER(_sClientReportControlBlock)


class IedConnectionException(Exception):
    def __init__(self, message: str, error_code: IedClientError, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.error_code})"


class IsoConnectionParameters: ...


class MmsConnection: ...


class MmsJournalEntry: ...


class MmsJournalVariable: ...


class MmsServerIdentity: ...


class IedConnection:
    """Represent a connection to an IED"""

    def __init__(self):
        self._handle = Wrapper.lib.IedConnection_create()
        self._state_changed_handler = None
        self._connection_closed_handler = None
        self._report_handlers = {}

    def __del__(self):
        Wrapper.lib.IedConnection_destroy(self._handle)

    ####################################################
    # Association service
    ####################################################

    def connect(self, hostname: str | bytes = b"localhost", port: int = 102):
        """Connect to the specified address"""
        hostname = convert_to_bytes(hostname)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_connect(self._handle, byref(_error), hostname, port)
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Connect command ", error)

    def abort(self):
        """Abort the connection."""
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_abort(self._handle, byref(_error))
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Abort command ", error)

    def release(self):
        """Release the connection.

        To be sure that the connection will be close the close or abort
        methods should be used.
        """
        Wrapper.lib.IedConnection_release(self._handle)

    def close(self):
        """Close the connection"""
        Wrapper.lib.IedConnection_close(self._handle)

    def set_connect_timeout(self, timeout: int):
        """set the connect timeout in ms

        Parameters
        ----------
        timeout : int
            Timeout in ms
        """
        Wrapper.lib.IedConnection_setConnectTimeout(self._handle, timeout)

    @property
    def status(self) -> IedConnectionState:
        """return the state of the connection.

        Returns
        -------
        IedConnectionState
            State of the connection
        """
        return IedConnectionState(Wrapper.lib.IedConnection_getState(self._handle))

    def get_last_appl_error(self) -> LastApplError:
        """Get the last received control application error

        Returns
        -------
        LastApplError
            Control application error
        """
        return Wrapper.lib.IedConnection_getLastApplError(self._handle)

    def on_connection_closed(
        self,
        fn: Callable[["IedConnection"], None],
    ) -> bool:
        """Set a callback which is trigger when the connection status change"""
        if self._connection_closed_handler is not None:
            return False
        self._connection_closed_handler = IedConnection_ClosedHandler(
            lambda parameter, connection: fn(self)
        )
        Wrapper.lib.IedConnection_installConnectionClosedHandler(
            self._handle, self._connection_closed_handler, None
        )
        return True

    def on_connection_state_change(
        self,
        fn: Callable[["IedConnection", IedConnectionState], None],
    ) -> bool:
        """Set a callback which is trigger when the connection status change"""
        if self._state_changed_handler is not None:
            return False
        self._state_changed_handler = IedConnection_StateChangedHandler(
            lambda parameter, connection, new_state: fn(self, IedConnectionState(new_state))
        )
        Wrapper.lib.IedConnection_installStateChangedHandler(
            self._handle, self._state_changed_handler, None
        )
        return True

    ####################################################
    # GOOSE services handling (MMS part)
    ####################################################

    ####################################################
    # ClientGooseControlBlock class
    ####################################################

    ####################################################
    # GOOSE services (access to GOOSE Control Blocks (GoCB))
    ####################################################

    def read_gocb(self, gocb_reference: str | bytes) -> "GooseControlBlock":
        """Create a ``GooseControlBlock`` by reading a reference on the server

        Parameters
        ----------
        gocb_reference : str | bytes
            Reference of the goose control block

        Returns
        -------
        GooseControlBlock
            _description_

        Raises
        ------
        IedConnectionException
            _description_
        """
        gocb_reference = convert_to_bytes(gocb_reference)
        _error = _cIedClientError(99)

        handle = Wrapper.lib.IedConnection_getGoCBValues(
            self._handle,
            byref(_error),
            gocb_reference,
            None,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading goose control block failed", error)

        return GooseControlBlock(handle)

    def update_gocb_values(self, gocb: "GooseControlBlock"):
        """Update values of a ReportControlBlock by reading values from the server

        Parameters
        ----------
        gocb : GooseControlBlock
            Goose control block to be updated

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)

        Wrapper.lib.IedConnection_getGoCBValues(
            self._handle,
            byref(_error),
            gocb.reference,
            gocb.handle,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading goose control block failed", error)
        gocb.clear_element_changed()

    def set_gocb_values(self, gocb: "GooseControlBlock", single_request: bool = True):
        """Send values of the GooseControlBlock to the server

        Parameters
        ----------
        gocb : GooseControlBlock
            _description_
        single_request : bool, optional
            _description_, by default True

        Raises
        ------
        IedConnectionException
            _description_
        """

        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_setGoCBValues(
            self._handle,
            byref(_error),
            gocb.reference,
            gocb.handle,
            gocb.element_changed.value,
            single_request,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Updating RCB values failed", error)
        gocb.clear_element_changed()

    ####################################################
    # Data model access services
    ####################################################

    def read_value(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
    ) -> MmsValue:
        """Read a functional constrained data attribute (FCDA) or functional constrained data (FCD).

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        MmsValue
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)

        handle = Wrapper.lib.IedConnection_readObject(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        if handle == 0:
            raise IedConnectionException("Variable not found on server", error)
        return MmsValue(handle, True)

    def write_value(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
        value: MmsValue,
    ):
        """Write a functional constrained data attribute (FCDA) or functional constrained data (FCD).

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to write
        fc : FunctionalConstraint
            Functional constraint of the data attribute to write
        value : MmsValue
            Value to write

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)

        Wrapper.lib.IedConnection_writeObject(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
            value.handle,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Write value failed", error)

    def read_boolean(self, object_reference: str | bytes, fc: FunctionalConstraint) -> bool:
        """Read a functional constrained data attribute (FCDA) of type bool.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        bool
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readBooleanValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return value

    def read_int32(self, object_reference: str | bytes, fc: FunctionalConstraint) -> int:
        """Read a functional constrained data attribute (FCDA) of type int32.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read, for example "IEDNameLD0/LLN0.Beh.stVal"
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        int
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readInt32Value(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return value

    def read_uint32(self, object_reference: str | bytes, fc: FunctionalConstraint) -> int:
        """Read a functional constrained data attribute (FCDA) of type uint32.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        int
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readUnsigned32Value(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return value

    def read_int64(self, object_reference: str | bytes, fc: FunctionalConstraint) -> int:
        """Read a functional constrained data attribute (FCDA) of type int64.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        int
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readInt64Value(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return value

    def read_float(self, object_reference: str | bytes, fc: FunctionalConstraint) -> float:
        """Read a functional constrained data attribute (FCDA) of type float.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read, for example "IEDNameLD0/PTOC1.StrVal.setMag.f"
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        float
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readFloatValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return value

    def read_string(self, object_reference: str | bytes, fc: FunctionalConstraint) -> bytes:
        """Read a functional constrained data attribute (FCDA) of type string.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        bytes
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readStringValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return value

    def read_timestamp(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
    ) -> Timestamp:
        """Read a functional constrained data attribute (FCDA) of type timestamp.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        Timestamp
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readTimestampValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return value  # TODO

    def read_quality(self, object_reference: str | bytes, fc: FunctionalConstraint) -> Quality:
        """Read a functional constrained data attribute (FCDA) of type Quality

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to read
        fc : FunctionalConstraint
            Functional constraint of the data attribute to read

        Returns
        -------
        Quality
            Value of the data attribute

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        value = Wrapper.lib.IedConnection_readQualityValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading value failed", error)
        return Quality(value)

    def write_boolean(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
        value: bool,
    ):
        """Write a functional constrained data attribute (FCDA) of type bool.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to write
        fc : FunctionalConstraint
            Functional constraint of the data attribute to write
        value : bool
            Value to write

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_writeBooleanValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
            value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Write value failed", error)

    def write_int32(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
        value: int,
    ):
        """Write a functional constrained data attribute (FCDA) of type int32.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to write
        fc : FunctionalConstraint
            Functional constraint of the data attribute to write
        value : int
            Value to write

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_writeInt32Value(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
            value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Write value failed", error)

    def write_uint32(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
        value: int,
    ):
        """Write a functional constrained data attribute (FCDA) of type uint32.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to write
        fc : FunctionalConstraint
            Functional constraint of the data attribute to write
        value : int
            Value to write

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_writeUnsigned32Value(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
            value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Write value failed", error)

    def write_float(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
        value: float,
    ):
        """Write a functional constrained data attribute (FCDA) of type float.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to write, for example "IEDNameLD0/PTOC1.StrVal.setMag.f"
        fc : FunctionalConstraint
            Functional constraint of the data attribute to write
        value : float
            Value to write

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_writeFloatValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
            value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Write value failed", error)

    def write_string(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
        value: str | bytes,
    ):
        """Write a functional constrained data attribute (FCDA) of type string.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to write
        fc : FunctionalConstraint
            Functional constraint of the data attribute to write
        value : str | bytes
            Value to write

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        value = convert_to_bytes(value)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_writeVisibleStringValue(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
            value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Write value failed", error)

    def write_octet_string(
        self,
        object_reference: str | bytes,
        fc: FunctionalConstraint,
        value: bytes,
    ):
        """Write a functional constrained data attribute (FCDA) of type octet string.

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the data attribute to write
        fc : FunctionalConstraint
            Functional constraint of the data attribute to write
        value : bytes
            Value to write

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_writeOctetString(
            self._handle,
            byref(_error),
            object_reference,
            fc.value,
            value,
            len(value),
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Write value failed", error)

    ####################################################
    # Reporting services
    ####################################################

    def read_rcb(self, rcb_reference: str | bytes) -> "ReportControlBlock":
        """Create a ReportControlBlock by reading a reference on the server

        Parameters
        ----------
        rcb_reference : str | bytes
            Reference of the report control block, for example "IEDNameLD0/LLN0.RP.URCBA"
            or "IEDNameLD0/LLN0.BR.BRCBA"

        Returns
        -------
        ReportControlBlock
            _description_

        Raises
        ------
        IedConnectionException
            _description_

        See also
        --------
        update_rcb_values
        """
        rcb_reference = convert_to_bytes(rcb_reference)
        _error = _cIedClientError(99)
        handle = Wrapper.lib.IedConnection_getRCBValues(
            self._handle,  # IedConnection,
            byref(_error),  # POINTER(IedClientError),
            rcb_reference,  # c_char_p,
            None,  # ClientReportControlBlock,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Get RCB values failed", error)
        return ReportControlBlock(handle, self)

    def update_rcb_values(self, rcb: "ReportControlBlock"):
        """Update values of a ReportControlBlock by reading values from the server

        Parameters
        ----------
        rcb : ReportControlBlock
            Report control block to be updated

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_getRCBValues(
            self._handle,  # IedConnection,
            byref(_error),  # POINTER(IedClientError),
            rcb.reference,  # c_char_p,
            rcb.handle,  # ClientReportControlBlock,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading RCB values failed", error)
        rcb.clear_element_changed()

    def set_rcb_values(self, rcb: "ReportControlBlock", single_request: bool = True):
        """Send values of the ReportControlBlock to the server

        Parameters
        ----------
        rcb : ReportControlBlock
            _description_
        single_request : bool, optional
            _description_, by default True

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_setRCBValues(
            self._handle,  # IedConnection self
            byref(_error),  # IedClientError* error
            rcb.handle,  # ClientReportControlBlock rcb
            rcb.element_changed.value,  # uint32_t parametersMask
            single_request,  # bool singleRequest
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Updating RCB values failed", error)
        rcb.clear_element_changed()

    def register_report_handler(
        self,
        rcb_reference: str | bytes,
        rpt_id: str | bytes,
        callback: Callable[["Report"], None],
    ):
        """Register a report callback function

        Parameters
        ----------
        rcb_reference : str | bytes
            Reference of the report control block
        rpt_id : str | bytes
            _description_
        callback : Callable[[Report], None]
            Callback function which is triggered every time a report is
            received

        See also
        --------
        unregister_report_handler
        """
        rcb_reference = convert_to_bytes(rcb_reference)
        rpt_id = convert_to_bytes(rpt_id)

        report_handler = ReportCallbackFunction(lambda parameter, report: callback(Report(report)))
        self._report_handlers[rcb_reference] = report_handler
        Wrapper.lib.IedConnection_installReportHandler(
            self._handle,
            rcb_reference,
            rpt_id,
            report_handler,
            None,
        )

    def unregister_report_handler(self, rcb_reference: str | bytes):
        """Unregister a report handler

        Parameters
        ----------
        rcb_reference : str | bytes
            Reference of the report control block

        See also
        --------
        register_report_handler
        """
        rcb_reference = convert_to_bytes(rcb_reference)
        Wrapper.lib.IedConnection_uninstallReportHandler(
            self._handle,  # IedConnection self
            rcb_reference,  # const char* rcbReference
        )

        self._report_handlers[rcb_reference] = None

    def create_rcb_and_subscribe(
        self,
        rcb_reference: str | bytes,
        callback: Callable[["Report"], None],
        trg_ops: ReportTriggerOptions | None = None,
        intg_pd: int | None = None,
        opt_flds: ReportOptions | None = None,
    ) -> "ReportControlBlock":
        """Helper function to create and subscribe a report control block

        Parameters
        ----------
        rcb_reference : str | bytes
            Reference of the report contro block
        callback : Callable[[Report], None]
            Callback function which is triggered every time a report is
            received
        trg_ops : ReportTriggerOptions | None, optional
            Trigger options to indicate when the report control block
            should generate a new report, by default None
        intg_pd : int | None, optional
            Integrity period for the report control block, by default None
        opt_flds : ReportOptions | None, optional
            Optional field that should be included in the report, by
            default None
        """
        rcb = self.read_rcb(rcb_reference)
        rcb.on_report(callback)
        rcb.subscribe(trg_ops, intg_pd, opt_flds)
        return rcb

    ####################################################
    # Data set handling
    ####################################################

    def read_dataset(self, dataset_reference: str | bytes) -> DataSet:
        """Create a DataSet by reading a reference on the server

        Parameters
        ----------
        dataset_reference : str | bytes
            Reference of the dataset, for example "IEDNameLD0/LLN0.DsRpt"

        Returns
        -------
        DataSet
            _description_

        Raises
        ------
        IedConnectionException
            _description_
        """
        dataset_reference = convert_to_bytes(dataset_reference)
        _error = _cIedClientError(99)
        handle = Wrapper.lib.IedConnection_readDataSetValues(
            self._handle,
            byref(_error),
            dataset_reference,
            None,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading dataset failed", error)
        return DataSet(handle, self)

    def update_dataset_values(self, dataset: DataSet):
        """Update the values stored in the dataset

        Parameters
        ----------
        dataset : DataSet
            _description_

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_readDataSetValues(
            self._handle,
            byref(_error),
            dataset.reference,
            dataset.handle,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Updating dataset value failed", error)

    def get_dataset_directory(self, dataset_reference: str | bytes) -> list[bytes]:
        """Return the list of reference of FCDA in the dataset

        Parameters
        ----------
        dataset_reference : str | bytes
            Reference of the dataset for example "IEDNameLD0/LLN0.DsRpt"

        Returns
        -------
        list[bytes]
            List of reference of FCDA in the dataset

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)
        is_deletable = c_bool(False)
        dataset_reference = convert_to_bytes(dataset_reference)
        head = Wrapper.lib.IedConnection_getDataSetDirectory(
            self._handle, byref(_error), dataset_reference, byref(is_deletable)
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Get dataset directory failed", error)
        return LinkedList(head).to_string_list()

    def create_dataset(self, dataset_reference: str | bytes, fcdas: list[str | bytes]):
        """Create a new data set at the connected server device

        This function creates a new data set at the server.

        Parameters
        ----------
        dataset_reference : str | bytes
            Name of the new data set to create. It is either in the form
            "LDName/LNodeName.dataSetName" for permanent domain or VMD
            scope data sets or @dataSetName for an association specific
            data set. If the LDName part of the reference is missing the
            resulting data set will be of VMD scope.
        fcdas : list[str | bytes]
            List of object references of FCDs or FCDAs. The format of this
            object references is
            "LDName/LNodeName.item(arrayIndex)component[FC]"

        Raises
        ------
        IedConnectionException
            _description_

        See also
        --------
        delete_dataset
        """
        dataset_reference = convert_to_bytes(dataset_reference)
        dataset_elements = LinkedList.create_from_string_list(fcdas)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_createDataSet(
            IedConnection,  # IedConnection self
            byref(_error),  # IedClientError* error
            dataset_reference,  # const char* dataSetReference
            dataset_elements.handle,  # LinkedList /* char* */ dataSetElements
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading dataset failed", error)

    def delete_dataset(self, dataset_reference: str | bytes):
        """Delete a deletable data set at the connected server device

        Parameters
        ----------
        dataset_reference : str | bytes
            Name of the new data set to delete. It is either in the form
            "LDName/LNodeName.dataSetName" for permanent domain or VMD
            scope data sets or @dataSetName for an association specific
            data set. If the LDName part of the reference is missing the
            resulting data set will be of VMD scope.

        Raises
        ------
        IedConnectionException
            _description_

        See also
        --------
        create_dataset
        """
        dataset_reference = convert_to_bytes(dataset_reference)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_deleteDataSet(
            IedConnection,  # IedConnection self
            byref(_error),  # IedClientError* error
            dataset_reference,  # const char* dataSetReference
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Reading dataset failed", error)

    ####################################################
    # Model discovery services
    ####################################################

    def get_logical_devices(self) -> list[bytes]:
        """Get the list of logical devices available at the server.

        Returns
        -------
        list[bytes]
            _description_

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)
        head = Wrapper.lib.IedConnection_getServerDirectory(self._handle, byref(_error), False)
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get logical devices", error)

        return LinkedList(head).to_string_list()

    def get_logical_nodes(self, logical_device_name: str | bytes) -> list[bytes]:
        """Get the list of logical nodes (LN) of a logical device.

        Parameters
        ----------
        logical_device_name : str | bytes
            Logical device name, for example "IEDNameLD0"

        Returns
        -------
        list[bytes]
            List of logical nodes

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)
        logical_device_name = convert_to_bytes(logical_device_name)
        head = Wrapper.lib.IedConnection_getLogicalDeviceDirectory(
            self._handle, byref(_error), logical_device_name
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get logical nodes", error)
        return LinkedList(head).to_string_list()

    def get_logical_node_directory(
        self,
        logical_node_reference: str | bytes,
        acsi_class: ACSIClass,
    ) -> list[bytes]:
        """Returns the directory of the given logical node (LN) containing elements of the specified ACSI class

        Parameters
        ----------
        logical_node_reference : str | bytes
            Logical node reference, for example "IEDNameLD0/LLN0"
        acsi_class : ACSIClass
            _description_

        Returns
        -------
        list[bytes]
            _description_

        Raises
        ------
        IedConnectionException
            _description_
        """
        _error = _cIedClientError(99)
        logical_node_reference = convert_to_bytes(logical_node_reference)

        head = Wrapper.lib.IedConnection_getLogicalNodeDirectory(
            self._handle,
            byref(_error),
            logical_node_reference,
            acsi_class.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get files", error)
        return LinkedList(head).to_string_list()

    def get_data_directory(self, data_reference: str | bytes) -> list[bytes]:
        """Returns the directory of the given data object (DO) or sub data objects.

        Parameters
        ----------
        data_reference : str | bytes
            Reference of the data object or sub dataobject, for example "IEDNameLD0/LLN0.Mod.Oper.origin"

        Returns
        -------
        list[bytes]
            List of all data attributes or sub data objects.

        Raises
        ------
        IedConnectionException
            _description_

        See Also
        --------
        get_data_directory_fc
        get_data_directory_by_fc
        """

        _error = _cIedClientError(99)
        data_reference = convert_to_bytes(data_reference)
        head = Wrapper.lib.IedConnection_getDataDirectory(
            self._handle,
            byref(_error),
            data_reference,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get data directory.", error)
        return LinkedList(head).to_string_list()

    def get_data_directory_fc(
        self,
        data_reference: str | bytes,
    ) -> list[bytes]:
        """Returns the directory of the given data object (DO) or sub data objects.

        Parameters
        ----------
        data_reference : str | bytes
            Reference of the data object or sub dataobject, for example "IEDNameLD0/LLN0.Mod.Oper.origin"

        Returns
        -------
        list[bytes]
            List of all data attributes or sub data objects with the functional constraint in square brackets.

        Raises
        ------
        IedConnectionException
            _description_

        See Also
        --------
        get_data_directory
        get_data_directory_by_fc
        """

        _error = _cIedClientError(99)
        data_reference = convert_to_bytes(data_reference)
        head = Wrapper.lib.IedConnection_getDataDirectoryFC(
            self._handle, byref(_error), data_reference
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get data directory.", error)
        return LinkedList(head).to_string_list()

    def get_data_directory_by_fc(
        self,
        data_reference: str | bytes,
        fc: FunctionalConstraint,
    ) -> list[bytes]:
        """Returns the directory of the given data object (DO) or sub data objects.

        Parameters
        ----------
        data_reference : str | bytes
            Reference of the data object or sub dataobject, for example "IEDNameLD0/LLN0.Mod"
        fc : FunctionalConstraint
            Functional constraint used to filter data attribute

        Returns
        -------
        list[bytes]
            List of all data attributes or sub data objects.

        Raises
        ------
        IedConnectionException
            _description_

        See Also
        --------
        get_data_directory
        get_data_directory_fc
        """
        _error = _cIedClientError(99)
        data_reference = convert_to_bytes(data_reference)

        head = Wrapper.lib.IedConnection_getDataDirectoryByFC(
            self._handle,
            byref(_error),
            data_reference,
            fc.value,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get data directory.", error)
        return LinkedList(head).to_string_list()

    def get_logical_device_variables(self, logical_device_name: str | bytes) -> list[bytes]:
        """Returns a list of all MMS variables that are children of the given logical device.

        Parameters
        ----------
        logical_device_name : str | bytes
            _description_

        Returns
        -------
        list[bytes]
            _description_

        Raises
        ------
        IedConnectionException
            _description_

        See Also
        --------
        get_logical_node_variables
        """

        _error = _cIedClientError(99)
        logical_device_name = convert_to_bytes(logical_device_name)
        head = Wrapper.lib.IedConnection_getLogicalDeviceVariables(
            self._handle, byref(_error), logical_device_name
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get logical devices variables.", error)
        return LinkedList(head).to_string_list()

    def get_logical_node_variables(self, logical_node_reference: str | bytes) -> list[bytes]:
        """Returns a list of all MMS variables that are children of the given logical node.

        Parameters
        ----------
        logical_node_reference : str | bytes
            Logical node reference, for example "IEDNameLD0/LLN0"

        Returns
        -------
        list[bytes]
            _description_

        Raises
        ------
        IedConnectionException
            _description_

        See Also
        --------
        get_logical_device_variables
        """
        _error = _cIedClientError(99)
        logical_node_reference = convert_to_bytes(logical_node_reference)
        head = Wrapper.lib.IedConnection_getLogicalNodeVariables(
            self._handle, byref(_error), logical_node_reference
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get logical node variables", error)
        return LinkedList(head).to_string_list()

    def get_logical_device_datasets(self, logical_device_name: str | bytes) -> list[bytes]:
        """Get the data set names of the logical device.

        NOTE: This function will return all data set names (MMS named variable lists) of the logical device (MMS domain). The result will be in the MMS notation (like "LLN0$dataset1").

        Parameters
        ----------
        logicalDeviceName : str
            _description_

        Returns
        -------
        list[str]
            _description_
        """
        _error = _cIedClientError(99)
        logical_device_name = convert_to_bytes(logical_device_name)
        head = Wrapper.lib.IedConnection_getLogicalDeviceDataSets(
            self._handle, byref(_error), logical_device_name
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get logical node variables", error)
        return LinkedList(head).to_string_list()

    ####################################################
    # File directory
    ####################################################
    def get_files(self, directory_name: str | bytes | None = None) -> list["FileDirectoryEntry"]:
        """Get the list of files available in the directory.

        Parameters
        ----------
        directory_name : str | bytes | None, optional
            _description_, by default None

        Returns
        -------
        list[bytes]
            _description_

        Raises
        ------
        IedConnectionException
            _description_
        """
        if directory_name:
            directory_name = convert_to_bytes(directory_name)
        _error = _cIedClientError(99)
        head = Wrapper.lib.IedConnection_getFileDirectory(
            self._handle,  # IedConnection self,
            byref(_error),  # IedClientError* error,
            directory_name,  # const char* directoryName
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to get file directory", error)
        handlers = LinkedList(head).to_pointer_list()
        return [FileDirectoryEntry(handler, self) for handler in handlers]

    def download_file(self, filename: str | bytes) -> bytearray:
        """Download the file

        Parameters
        ----------
        filename : str | bytes
            _description_

        Returns
        -------
        bytearray
            Return content of the file
        """
        filename = convert_to_bytes(filename)
        _error = _cIedClientError(99)
        buffer = bytearray()

        def _on_byte_received(parameter: None, buffer_ptr, bytes_read: int) -> bool:
            data = ctypes.string_at(buffer_ptr, bytes_read)
            buffer.extend(data)

            return True

        handler = IedClientGetFileHandler(_on_byte_received)
        Wrapper.lib.IedConnection_getFile(
            self._handle,  # IedConnection self,
            byref(_error),  # IedClientError* error,
            filename,  # const char* fileName,
            handler,  # IedClientGetFileHandler handler,
            None,  # void* handlerParameter
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException(f"Failed to download file {filename}", error)
        return buffer

    def set_filestore_basepath(self, basepath: str | bytes):
        """Set the base directory for the file service

        Parameters
        ----------
        basepath : str | bytes
            _description_
        """
        basepath = convert_to_bytes(basepath)
        Wrapper.lib.IedConnection_setFilestoreBasepath(
            self._handle,  # IedConnection self,
            basepath,  # const char* basepath
        )

    def upload_file(self, source_filename: str | bytes, destination_filename: str | bytes):
        """Upload a file (from the local filestore) to the server

        Parameters
        ----------
        source_filename : str | bytes
            Local file name relative to the basepath of the filestore
        destination_filename : str | bytes
            Name of the file in the server

        See Also
        --------
        set_filestore_basepath
        """
        source_filename = convert_to_bytes(source_filename)
        destination_filename = convert_to_bytes(destination_filename)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_setFile(
            self._handle,  # IedConnection self,
            byref(_error),  # IedClientError* error,
            source_filename,  # const char* sourceFilename,
            destination_filename,  # const char* destinationFilename
        )

    def delete_file(self, filename: str | bytes):
        """Delete the file on the server

        Parameters
        ----------
        filename : str | bytes
            _description_

        Raises
        ------
        IedConnectionException
            _description_
        """
        filename = convert_to_bytes(filename)
        _error = _cIedClientError(99)
        Wrapper.lib.IedConnection_deleteFile(
            self._handle,  # IedConnection self,
            byref(_error),  # IedClientError* error,
            filename,  # const char* fileName,
        )
        error = IedClientError(_error.value)
        if error != IedClientError.OK:
            raise IedConnectionException("Failed to delete file", error)

    ####################################################
    # Control
    ####################################################

    def read_control(self, object_reference: str | bytes) -> ControlObject:
        """Read a controlable data object from the server

        Parameters
        ----------
        object_reference : str | bytes
            Reference of the controllable data object, for example "IEDNameLD0/LLN0.Mod"

        Returns
        -------
        ControlObject
            Control object

        Raises
        ------
        IedConnectionException
            _description_
        """
        object_reference = convert_to_bytes(object_reference)
        handle = Wrapper.lib.ControlObjectClient_create(object_reference, self._handle)
        if not handle:
            raise IedConnectionException(
                "Reading object failed",
                IedClientError.OBJECT_DOES_NOT_EXIST,
            )
        return ControlObject(handle)
