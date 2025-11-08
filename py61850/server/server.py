"""Server API"""

import ctypes
import datetime
from collections.abc import Callable
from enum import Enum, Flag
from typing import TYPE_CHECKING, Literal

from ..binding.iec61850.model import DataAttribute as _cDataAttribute
from ..binding.iec61850.model import DataObject as _cDataObject
from ..binding.iec61850.model import IedModel as _cIedModel
from ..binding.iec61850.model import LogicalDevice as _cLogicalDevice
from ..binding.iec61850.model import ModelNode as _cModelNode
from ..binding.iec61850.model import (
    SettingGroupControlBlock as _cSettingGroupControlBlock,
)
from ..binding.iec61850.server import (
    ActiveSettingGroupChangedHandler,
    ControlHandler,
    ControlPerformCheckHandler,
    ControlSelectStateChangedHandler,
    ControlWaitForExecutionHandler,
    EditSettingGroupChangedHandler,
    EditSettingGroupConfirmationHandler,
    GoCBEventHandler,
    IedConnectionIndicationHandler,
    IedServer_ControlBlockAccessHandler,
    IedServer_DataSetAccessHandler,
    IedServer_DirectoryAccessHandler,
    IedServer_ListObjectsAccessHandler,
    IedServer_RCBEventHandler,
    ReadAccessHandler,
    SVCBEventHandler,
    WriteAccessHandler,
)
from ..binding.loader import Wrapper
from ..binding.mms import MmsValue as _cMmsValue
from ..common import (
    ControlAddCause,
    ControlLastApplError,
    Dbpos,
    FunctionalConstraint,
    Iec61850Edition,
    MmsDataAccessError,
    MmsValue,
    OrCat,
    Quality,
    Timestamp,
)
from ..helper import (
    address_of,
    convert_to_bytes,
    convert_to_datetime,
    convert_to_uint64,
)
from .model import (
    AccessPolicy,
    CheckHandlerResult,
    ControlHandlerResult,
    DataAttribute,
    DataObject,
    IedModel,
    SelectStateChangedReason,
    SettingGroupControlBlock,
)

__all__ = []


if TYPE_CHECKING:
    Pointer = ctypes._Pointer
    IedModelPointer = ctypes._Pointer[_cIedModel]
    ModelNodePointer = ctypes._Pointer[_cModelNode]
    LogicalDevicePointer = ctypes._Pointer[_cLogicalDevice]
    DataObjectPointer = ctypes._Pointer[_cDataObject]
    DataAttributePointer = ctypes._Pointer[_cDataAttribute]
    SGCBPointer = ctypes._Pointer[_cSettingGroupControlBlock]
    MmsValuePointer = ctypes._Pointer[_cMmsValue]
else:
    Pointer = ctypes.POINTER
    IedModelPointer = ctypes.POINTER(_cIedModel)
    ModelNodePointer = ctypes.POINTER(_cModelNode)
    LogicalDevicePointer = ctypes.POINTER(_cLogicalDevice)
    DataObjectPointer = ctypes.POINTER(_cDataObject)
    DataAttributePointer = ctypes.POINTER(_cDataAttribute)
    SGCBPointer = ctypes.POINTER(_cSettingGroupControlBlock)
    MmsValuePointer = ctypes.POINTER(_cMmsValue)


class IedServer_RCBEventType(Enum):
    GET_PARAMETER = 0
    """parameter read by client (not implemented)"""
    SET_PARAMETER = 1
    """parameter set by client"""
    UNRESERVED = 2
    """RCB reservation canceled"""
    RESERVED = 3
    """RCB reserved"""
    ENABLE = 4
    """RCB enabled"""
    DISABLE = 5
    """RCB disabled"""
    GI = 6
    """GI report triggered"""
    PURGEBUF = 7
    """Purge buffer procedure executed"""
    OVERFLOW = 8
    """Report buffer overflow"""
    REPORT_CREATED = 9
    """A new report was created and inserted into the buffer"""


class IedServer_DataSetOperation(Enum):
    CREATE = 0
    DELETE = 1
    READ = 2
    WRITE = 3
    GET_DIRECTORY = 4


class IedServer_DirectoryCategory(Enum):
    LD_LIST = 0
    DATA_LIST = 1
    DATASET_LIST = 2
    LOG_LIST = 3


class IedServer_ControlBlockAccessType(Enum):
    READ = 0
    WRITE = 1


class ReportSetting(Flag):
    RPT_ID = 1
    BUF_TIME = 2
    DATSET = 4
    TRG_OPS = 8
    OPT_FIELDS = 16
    INTG_PD = 32


class ClientConnection:
    """Client connection with a server"""

    def __init__(self, handle: int) -> None:
        self._handle = handle

    def local_address(self) -> bytes:
        return Wrapper.lib.ClientConnection_getPeerAddress(self._handle)

    def peer_address(self) -> bytes:
        return Wrapper.lib.ClientConnection_getLocalAddress(self._handle)

    def abort(self):
        Wrapper.lib.ClientConnection_abort(self._handle)

    def release(self):
        Wrapper.lib.ClientConnection_release(self._handle)

        # Wrapper.lib.ClientConnection_claimOwnership.argtypes = [
        #     ClientConnection,  # ClientConnection self
        # ]
        # Wrapper.lib.ClientConnection_claimOwnership.restype = ClientConnection

        # Wrapper.lib.ClientConnection_getSecurityToken.argtypes = [
        #     ClientConnection,  # ClientConnection self
        # ]
        # Wrapper.lib.ClientConnection_getSecurityToken.restype = c_void_p

    @property
    def addressof(self) -> int:
        """Address of the underlying C structure"""
        return self._handle


class ControlAction:
    """Provide additional information on a control action from a client"""

    def __init__(self, handle: ctypes.c_void_p) -> None:
        self._handle = handle

    def set_error(self, error: ControlLastApplError):
        """Sets the error code for the next command termination or application error message.

        Parameters
        ----------
        error : ControlLastApplError
            _description_
        """
        Wrapper.lib.ControlAction_setError(self._handle, error.value)

    def set_add_cause(self, add_cause: ControlAddCause):
        """Sets the add cause for the next command termination or application error message.

        Parameters
        ----------
        add_cause : ControlAddCause
            _description_
        """
        Wrapper.lib.ControlAction_setAddCause(self._handle, add_cause.value)

    def get_originator_category(self) -> OrCat:
        """Gets the originator category provided by the client.

        Returns
        -------
        OrCat
            _description_
        """
        value = Wrapper.lib.ControlAction_getOrCat(self._handle)
        return OrCat(value)

    def get_originator_identifier(self) -> bytes:
        """Gets the originator identifier provided by the client.

        Returns
        -------
        bytes
            _description_
        """
        or_ident_size = ctypes.c_int(0)
        ptr = Wrapper.lib.ControlAction_getOrIdent(self._handle, ctypes.byref(or_ident_size))
        if not ptr:
            return b""
        array_type = ctypes.c_uint8 * or_ident_size.value
        array = ctypes.cast(ptr, ctypes.POINTER(array_type)).contents
        return bytes(array)

    def get_ctl_num(self) -> int:
        """Get the ctlNum attribute send by the client.

        Returns
        -------
        int
            _description_
        """
        return Wrapper.lib.ControlAction_getCtlNum(self._handle)

    def get_synchro_check(self) -> bool:
        """Gets the synchroCheck bit provided by the client.

        Returns
        -------
        bool
            _description_
        """
        return Wrapper.lib.ControlAction_getSynchroCheck(self._handle)

    def get_interlock_check(self) -> bool:
        """Gets the interlockCheck bit provided by the client.

        Returns
        -------
        bool
            _description_
        """
        return Wrapper.lib.ControlAction_getInterlockCheck(self._handle)

    def is_select(self) -> bool:
        """Check if the control callback is called by a select or operate command.

        Returns
        -------
        bool
            _description_
        """
        return Wrapper.lib.ControlAction_isSelect(self._handle)

    def get_client_connection(self) -> ClientConnection:
        """Gets the client object associated with the client that caused the control action.

        Returns
        -------
        ClientConnection
            _description_
        """
        handle = Wrapper.lib.ControlAction_getClientConnection(self._handle)
        return ClientConnection(handle)

    def get_control_object(self) -> DataObject:
        """Gets the control object that is subject to this action.

        Returns
        -------
        DataObject
            _description_
        """
        handle = Wrapper.lib.ControlAction_getControlObject(self._handle)
        return DataObject(handle)

    def get_control_time(self) -> datetime.datetime | None:
        """Gets the time of the control (attribute "operTm").

        Returns
        -------
        datetime.datetime | None
            None when it is not a timeActivatedControl
        """
        ms = Wrapper.lib.ControlAction_getControlTime(self._handle)
        if ms > 0:
            return convert_to_datetime(ms)
        return None

    def getT(self) -> Timestamp:
        """Gets the time (attribute "T") of the last received control action (Oper or Select)

        Returns
        -------
        Timestamp
            _description_
        """
        handle = Wrapper.lib.ControlAction_getT(self._handle)
        return Timestamp(handle)


class IedServerConfig:
    """IedServer configuration object"""

    def __init__(self) -> None:
        self._handle = Wrapper.lib.IedServerConfig_create()

    def __del__(self):
        Wrapper.lib.IedServerConfig_destroy(self._handle)

    @property
    def handle(self):
        """Pointer to the underlying C structure"""
        return self._handle

    @property
    def edition(self) -> Iec61850Edition:
        """Configured IEC 61850 standard edition."""
        return Iec61850Edition(Wrapper.lib.IedServerConfig_getEdition(self._handle))

    @edition.setter
    def edition(self, value: Iec61850Edition):
        Wrapper.lib.IedServerConfig_setEdition(self._handle, value.value)

    @property
    def report_buffer_size_brcb(self) -> int:
        """Report buffer size for buffered reporting."""
        return Wrapper.lib.IedServerConfig_getReportBufferSize(self._handle)

    @report_buffer_size_brcb.setter
    def report_buffer_size_brcb(self, value: int):
        Wrapper.lib.IedServerConfig_setReportBufferSize(self._handle, value)

    @property
    def report_buffer_size_urcb(self) -> int:
        """Report buffer size for unbuffered reporting."""
        return Wrapper.lib.IedServerConfig_getReportBufferSizeForURCBs(self._handle)

    @report_buffer_size_urcb.setter
    def report_buffer_size_urcb(self, value: int):
        Wrapper.lib.IedServerConfig_setReportBufferSizeForURCBs(self._handle, value)

    @property
    def max_mms_connection(self) -> int:
        """Maximum number of MMS (TCP) connections the server accepts."""
        return Wrapper.lib.IedServerConfig_getMaxMmsConnections(self._handle)

    @max_mms_connection.setter
    def max_mms_connection(self, value: int):
        Wrapper.lib.IedServerConfig_setMaxMmsConnections(self._handle, value)

    @property
    def sync_integrity_report_times(self) -> bool:
        """Synchronize integrity report times."""
        return Wrapper.lib.IedServerConfig_getSyncIntegrityReportTimes(self._handle)

    @sync_integrity_report_times.setter
    def sync_integrity_report_times(self, value: bool):
        Wrapper.lib.IedServerConfig_setSyncIntegrityReportTimes(self._handle, value)

    @property
    def file_service_enabled(self) -> bool:
        """File services status."""
        return Wrapper.lib.IedServerConfig_isFileServiceEnabled(self._handle)

    @file_service_enabled.setter
    def file_service_enabled(self, value: bool):
        Wrapper.lib.IedServerConfig_enableFileService(self._handle, value)

    @property
    def file_service_base_path(self) -> bytes:
        """Basepath of the file services."""
        return Wrapper.lib.IedServerConfig_getFileServiceBasePath(self._handle)

    @file_service_base_path.setter
    def file_service_base_path(self, value: str | bytes):
        value = convert_to_bytes(value)
        Wrapper.lib.IedServerConfig_setFileServiceBasePath(self._handle, value)

    @property
    def dynamic_dataset_enabled(self) -> bool:
        """Dynamic dataset support."""
        return Wrapper.lib.IedServerConfig_isDynamicDataSetServiceEnabled(self._handle)

    @dynamic_dataset_enabled.setter
    def dynamic_dataset_enabled(self, value: bool):
        Wrapper.lib.IedServerConfig_enableDynamicDataSetService(self._handle, value)

    @property
    def max_association_specific_datasets(self) -> int:
        """Maximum allowed number of association specific (non-permanent) data sets."""
        return Wrapper.lib.IedServerConfig_getMaxAssociationSpecificDataSets(self._handle)

    @max_association_specific_datasets.setter
    def max_association_specific_datasets(self, value: int):
        Wrapper.lib.IedServerConfig_setMaxAssociationSpecificDataSets(self._handle, value)

    @property
    def max_domain_specific_datasets(self) -> int:
        """Maximum allowed number of domain specific (permanent) data sets."""
        return Wrapper.lib.IedServerConfig_getMaxDomainSpecificDataSets(self._handle)

    @max_domain_specific_datasets.setter
    def max_domain_specific_datasets(self, value: int):
        Wrapper.lib.IedServerConfig_setMaxDomainSpecificDataSets(self._handle, value)

    @property
    def max_dataset_entries(self) -> int:
        """Maximum number of entries in dynamic data sets."""
        return Wrapper.lib.IedServerConfig_getMaxDatasSetEntries(self._handle)

    @max_dataset_entries.setter
    def max_dataset_entries(self, value: int):
        Wrapper.lib.IedServerConfig_setMaxDataSetEntries(self._handle, value)

    @property
    def log_service_enabled(self) -> bool:
        """Log services status."""
        return Wrapper.lib.IedServerConfig_isLogServiceEnabled(self._handle)

    @log_service_enabled.setter
    def log_service_enabled(self, value: bool):
        Wrapper.lib.IedServerConfig_enableLogService(self._handle, value)

    def edit_sg_enabled(self, value: bool):
        """Allow clients to change setting groups"""
        Wrapper.lib.IedServerConfig_enableEditSG(self._handle, value)

    def enable_resv_tms_sgcb(self, value: bool):
        """Enable/disable the SGCB.ResvTms when EditSG is enabled"""
        Wrapper.lib.IedServerConfig_enableResvTmsForSGCB(self._handle, value)

    @property
    def enable_resv_tms_brcb(self) -> bool:
        """Enable/disable the presence of BRCB.ResvTms."""
        return Wrapper.lib.IedServerConfig_isResvTmsForBRCBEnabled(self._handle)

    @enable_resv_tms_brcb.setter
    def enable_resv_tms_brcb(self, value: bool):
        Wrapper.lib.IedServerConfig_enableResvTmsForBRCB(self._handle, value)

    @property
    def enable_owner_for_rcb(self) -> bool:
        """Owner for RCBs enabled (visible)."""
        return Wrapper.lib.IedServerConfig_isOwnerForRCBEnabled(self._handle)

    @enable_owner_for_rcb.setter
    def enable_owner_for_rcb(self, value: bool):
        Wrapper.lib.IedServerConfig_enableOwnerForRCB(self._handle, value)

    def use_integrated_goose_publisher(self, value: bool):
        """Enable/disable using the integrated GOOSE publisher for configured GoCBs.

        Parameters
        ----------
        value : bool
            _description_
        """
        Wrapper.lib.IedServerConfig_useIntegratedGoosePublisher(self._handle, value)

    def set_report_setting(self, setting: ReportSetting, is_dyn: bool):
        """Make a configurable report setting writeable or read-only.

        Parameters
        ----------
        setting : ReportSetting
            _description_
        is_dyn : bool
            _description_
        """

        Wrapper.lib.IedServerConfig_setReportSetting(self._handle, setting, is_dyn)

    def get_report_setting(self, setting: ReportSetting) -> bool:
        """Check if a configurable report setting is writable or read-only.

        Parameters
        ----------
        setting : ReportSetting
            _description_

        Returns
        -------
        bool
            _description_
        """
        return Wrapper.lib.IedServerConfig_getReportSetting(self._handle, setting)


class IedServer:
    """IED server instance"""

    def __init__(self, ied_model: IedModel, config: IedServerConfig | None = None):
        self._ied_model = ied_model
        self._config = config
        self._client_connections: dict[int, ClientConnection] = {}
        self._sgcbs: dict[int, SettingGroupControlBlock] = {}
        self._data_objects: dict[int, DataObject] = {}
        self._data_attributes: dict[int, DataAttribute] = {}

        self._handle = Wrapper.lib.IedServer_createWithConfig(
            ied_model.handle,
            None,
            None if config is None else config.handle,
        )

        self._connection_handler = IedConnectionIndicationHandler(self._connection_handler_fn)

        self._active_setting_group_changed_handlers = {}
        self._edit_setting_group_changed_handlers = {}
        self._edit_setting_group_confirmed_handlers = {}

        self._control_static_check_handlers = {}
        self._control_wait_handlers = {}
        self._control_handlers = {}
        self._control_select_handlers = {}

        # self._connection_handler = IedServer_RCBEventHandler(self._connection_handler_fn)
        # self._connection_handler = SVCBEventHandler(self._connection_handler_fn)
        # self._connection_handler = GoCBEventHandler(self._connection_handler_fn)
        self._write_handlers = {}
        self._read_handlers = {}  # ReadAccessHandler(self._connection_handler_fn)
        # self._connection_handler = IedServer_DataSetAccessHandler(self._connection_handler_fn)
        # self._connection_handler = IedServer_DirectoryAccessHandler(self._connection_handler_fn)
        # self._connection_handler = IedServer_ListObjectsAccessHandler(self._connection_handler_fn)
        # self._connection_handler = IedServer_ControlBlockAccessHandler(self._connection_handler_fn)

        self._on_connection_change: Callable[[ClientConnection, bool], None] | None = None

        Wrapper.lib.IedServer_setConnectionIndicationHandler(
            self._handle, self._connection_handler, None
        )

    def start(self, port: int = 102):
        """Start handling client connections.

        Parameters
        ----------
        port : int, optional
            TCP port the server is listening, by default 102
        """
        Wrapper.lib.IedServer_start(self._handle, port)

    def stop(self):
        """Stop the server"""
        Wrapper.lib.IedServer_stop(self._handle)

    @property
    def is_running(self) -> bool:
        """Check if IedServer instance is listening for client connections."""
        return Wrapper.lib.IedServer_isRunning(self._handle)

    def _connection_handler_fn(
        self,
        ied_server_handle: int,  # IedServer
        connection_handle: int,  # ClientConnection
        connected: bool,
        parameter: int | None,
    ):
        if connected:
            # A client is connected
            client_connection = ClientConnection(connection_handle)
            self._client_connections.setdefault(address_of(connection_handle), client_connection)
        else:
            # A client is disconnected
            client_connection = self._client_connections.pop(address_of(connection_handle))

        if self._on_connection_change is not None:
            self._on_connection_change(client_connection, connected)

    def register_connection_change(self, callback: Callable[[ClientConnection, bool], None]):
        """Set a callback function that will be called on connection events (open or close).

        Parameters
        ----------
        callback : Callable[[ClientConnection, bool], None]
            Callback function with ClientConnection object and connected status (True on conected
            event, False on disconnected event)
        """
        self._on_connection_change = callback

    def register_active_setting_group_change_handler(
        self,
        sgcb: SettingGroupControlBlock,
        callback: Callable[[SettingGroupControlBlock, ClientConnection, int], bool],
    ):
        """Set the callback handler when ActSG is changed

        Parameters
        ----------
        sgcb : SettingGroupControlBlock
            Setting group control block
        callback : Callable[[SettingGroupControlBlock, ClientConnection, int], bool]
            The callback should return True to confirm the change, False otherwise.
        """

        self._sgcbs[sgcb.addressof] = sgcb

        def fun(
            parameter: int | None,  # void*
            sgcb_handle: SGCBPointer,
            new_active_setting_group: int,
            connection_handle: int,  # ClientConnection
        ) -> bool:
            sgcb = self._sgcbs[address_of(sgcb_handle)]
            client_connection = self._client_connections[address_of(connection_handle)]
            return callback(sgcb, client_connection, new_active_setting_group)

        handler = ActiveSettingGroupChangedHandler(fun)
        Wrapper.lib.IedServer_setActiveSettingGroupChangedHandler(
            self._handle,
            sgcb.handle,
            handler,
            None,
        )
        self._active_setting_group_changed_handlers[sgcb.addressof] = handler  # type: ignore

    def register_edit_setting_group_change_handler(
        self,
        sgcb: SettingGroupControlBlock,
        callback: Callable[[SettingGroupControlBlock, ClientConnection, int], bool],
    ):
        """Set the callback handler when EditSG is changed

        Parameters
        ----------
        sgcb : SettingGroupControlBlock
            Setting group control block
        callback : Callable[[SettingGroupControlBlock, ClientConnection, int], bool]
            The callback should return True to confirm the change, False otherwise.
        """
        self._sgcbs[sgcb.addressof] = sgcb

        def fun(
            parameter: int | None,  # void*
            sgcb_handle: SGCBPointer,
            new_edit_setting_group: int,
            connection_handle: int,  # ClientConnection
        ) -> bool:
            sgcb = self._sgcbs[address_of(sgcb_handle)]
            client_connection = self._client_connections[address_of(connection_handle)]
            return callback(sgcb, client_connection, new_edit_setting_group)

        handler = EditSettingGroupChangedHandler(fun)
        Wrapper.lib.IedServer_setEditSettingGroupChangedHandler(
            self._handle,
            sgcb.handle,
            handler,
            None,
        )
        self._edit_setting_group_changed_handlers[sgcb.addressof] = handler  # type: ignore

    def register_edit_setting_group_confirmed_handler(
        self,
        sgcb: SettingGroupControlBlock,
        callback: Callable[[SettingGroupControlBlock, int], None],
    ):
        """Set the callback handler when CnfEdit is set to True

        Parameters
        ----------
        sgcb : SettingGroupControlBlock
            Setting group control block
        callback : Callable[[SettingGroupControlBlock, int], bool]
            The callback should return True to confirm the change, False otherwise.
        """
        self._sgcbs[sgcb.addressof] = sgcb

        def fun(
            parameter: int | None,  # void*
            sgcb_handle: SGCBPointer,
            edit_setting_group: int,
        ):
            sgcb = self._sgcbs[address_of(sgcb_handle)]
            callback(sgcb, edit_setting_group)

        handler = EditSettingGroupConfirmationHandler(fun)
        Wrapper.lib.IedServer_setEditSettingGroupConfirmationHandler(
            self._handle,
            sgcb.handle,
            handler,
            None,
        )
        self._edit_setting_group_confirmed_handlers[sgcb.addressof] = handler  # type: ignore

    def register_control_handler(
        self,
        data_object: DataObject,
        callback: Callable[[DataObject, ControlAction, MmsValue, bool], ControlHandlerResult],
    ):
        """Set control handler for controllable data object.

        The control handler is a callback function that will be called by
        the IEC server when a client invokes a control operation on the
        data object.

        Parameters
        ----------
        data_object : DataObject
            Data object, has to be an instance of a controllable CDC
            (Common Data Class) like e.g. SPC, DPC or APC.
        callback : Callable[[DataObject, ControlAction, MmsValue, bool], ControlHandlerResult]
            Callback function
        """
        self._data_objects[data_object.addressof] = data_object

        def fun(
            action: int,  # ControlAction action
            parameter: int,  # void*  #  void* parameter,
            ctl_val: MmsValuePointer,  # MmsValue* ctlVal
            test: bool,
        ) -> int:  # bool test
            data_object = self._data_objects[address_of(parameter)]
            return callback(data_object, ControlAction(action), MmsValue(ctl_val), test).value

        handler = ControlHandler(fun)
        Wrapper.lib.IedServer_setControlHandler(
            self._handle,
            data_object.handle,
            handler,
            data_object.handle,  # parameter
        )
        self._control_handlers[data_object.addressof] = handler  # type: ignore

    def register_control_static_check_handler(
        self,
        data_object: DataObject,
        callback: Callable[[DataObject, ControlAction, MmsValue, bool, bool], CheckHandlerResult],
    ):
        """Set a handler for a controllable data object to perform operative tests.

        The callback is called for select and operate commant.

        This functions sets a user provided handler that should perform
        the operative tests for a control operation. Setting this handler
        is not required. If not set the server assumes that the checks
        will always be successful. The handler has to return true upon a
        successful test of false if the test fails. In the later case the
        control operation will be aborted.

        Parameters
        ----------
        data_object : DataObject
            Data object, has to be an instance of a controllable CDC
            (Common Data Class) like e.g. SPC, DPC or APC.
        callback : Callable[[DataObject, ControlAction, MmsValue, bool, bool], CheckHandlerResult]
            Callback function
        """
        self._data_objects[data_object.addressof] = data_object

        def fun(
            action: int,  # ControlAction action,
            parameter: int,  # void*  #  void* parameter,
            ctl_val: MmsValuePointer,  # MmsValue* ctlVal
            test: bool,  # bool test
            interlock_check: bool,  # bool interlockCheck
        ) -> int:
            data_object = self._data_objects[address_of(parameter)]
            return callback(
                data_object,
                ControlAction(action),
                MmsValue(ctl_val),
                test,
                interlock_check,
            ).value

        handler = ControlPerformCheckHandler(fun)
        Wrapper.lib.IedServer_setPerformCheckHandler(
            self._handle,
            data_object.handle,
            handler,
            data_object.handle,  # parameter
        )
        self._control_static_check_handlers[callback] = handler  # type: ignore

    def register_control_wait_handler(
        self,
        data_object: DataObject,
        callback: Callable[
            [DataObject, ControlAction, MmsValue, bool, bool],
            ControlHandlerResult,
        ],
    ):
        """Set a handler for a controllable data object to perform dynamic tests.

        The callback is only called for operate commant.

        This functions sets a user provided handler that should perform
        the dynamic tests for a control operation. Setting this handler is
        not required. If not set the server assumes that the checks will
        always be successful. The handler has to return true upon a
        successful test of false if the test fails. In the later case the
        control operation will be aborted.

        Parameters
        ----------
        data_object : DataObject
            Data object, has to be an instance of a controllable CDC
            (Common Data Class) like e.g. SPC, DPC or APC.
        callback : Callable[[DataObject, ControlAction, MmsValue, bool, bool], ControlHandlerResult]
            Callback function
        """
        self._data_objects[data_object.addressof] = data_object

        def fun(
            action: int,  # ControlAction action,
            parameter: int,  # void*  #  void* parameter,
            ctl_val: MmsValuePointer,  # MmsValue* ctlVal
            test: bool,  # bool test
            interlock_check: bool,  # bool interlockCheck
        ) -> int:
            data_object = self._data_objects[address_of(parameter)]
            return callback(
                data_object,
                ControlAction(action),
                MmsValue(ctl_val),
                test,
                interlock_check,
            ).value

        handler = ControlWaitForExecutionHandler(fun)
        Wrapper.lib.IedServer_setWaitForExecutionHandler(
            self._handle,
            data_object.handle,
            handler,
            data_object.handle,  # parameter
        )
        self._control_wait_handlers[callback] = handler  # type: ignore

    def register_control_select_state_handler(
        self,
        data_object: DataObject,
        callback: Callable[
            [DataObject, ControlAction, bool, SelectStateChangedReason],
            None,
        ],
    ):
        """Set a callback handler for a controllable data object to track select state changes.

        The callback is called whenever the select state of a control
        changes. Reason for changes can be:

        - a successful select or select-with-value by a client
        - select timeout
        - operate or failed operate
        - cancel request by a client
        - the client that selected the control has been disconnected

        Parameters
        ----------
        data_object : DataObject
            Data object, has to be an instance of a controllable
            CDC (Common Data Class) like e.g. SPC, DPC or APC.
        callback : Callable[ [DataObject, ControlAction, bool, SelectStateChangedReason], None, ]
            Callback function
        """
        self._data_objects[data_object.addressof] = data_object

        def fun(
            action: int,  # ControlAction action,
            parameter: int | None,  # void*  #  void* parameter,
            is_selected: bool,  # bool isSelected,
            reason: int,  # SelectStateChangedReason reason
        ):
            callback(
                data_object,
                ControlAction(action),
                is_selected,
                SelectStateChangedReason(reason),
            )

        handler = ControlSelectStateChangedHandler(fun)
        Wrapper.lib.IedServer_setSelectStateChangedHandler(
            self._handle,
            data_object.handle,
            handler,
            None,
        )
        self._control_select_handlers[callback] = handler  # type: ignore

    def register_write_handler(
        self,
        data_attribute: DataAttribute,
        callback: Callable[[ClientConnection, DataAttribute, MmsValue], MmsDataAccessError],
    ):
        """Install an optional write access handler for a data attribute.

        This instructs the server to monitor write attempts by MMS clients
        to specific data attributes. If a client tries to write to the
        monitored data attribute the handler is invoked. The handler can
        decide if the write access will be allowed or denied. If a
        write access handler is set for a specific data attribute - the
        default write access policy will not be performed for that data
        attribute.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        callback : Callable[[ClientConnection, DataAttribute, MmsValue], MmsDataAccessError]
            Callback function which return the reponse type to the client
        """
        self._data_attributes[data_attribute.addressof] = data_attribute

        def fun(
            data_attribute_ptr: DataAttributePointer,  # DataAttribute* dataAttribute
            value_ptr: MmsValuePointer,  # MmsValue* value,
            connection_handle: int,  #  ClientConnection connection,
            parameter: int | None,  # void*  # void* parameter
        ) -> int:  # MmsDataAccessError
            client_connection = self._client_connections[address_of(connection_handle)]
            data_attribute = self._data_attributes[address_of(data_attribute_ptr)]
            return callback(
                client_connection,
                data_attribute,
                MmsValue(value_ptr),
            ).value

        handler = WriteAccessHandler(fun)
        Wrapper.lib.IedServer_handleWriteAccess(
            self._handle,
            data_attribute.handle,
            handler,
            None,
        )
        self._write_handlers[callback] = handler  # type: ignore

    def get_value(self, data_attribute: DataAttribute) -> MmsValue | None:
        """Get data attribute value.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        MmsValue | None
            MmsValue object of the MMS Named Variable or None if the value does not exist.
        """
        handle = Wrapper.lib.IedServer_getAttributeValue(self._handle, data_attribute.handle)
        if handle:
            return MmsValue(handle)
        return None

    def get_value_with_fc(
        self, data_object: DataObject, fc: FunctionalConstraint
    ) -> MmsValue | None:
        """Get the MmsValue object related to a functional constrained data object (FCD)

        Get the MmsValue from the server cache that is associated with the
        Functional Constrained Data (FCD) object that is specified by the
        DataObject and the given Function Constraint (FC). Accessing the
        value will directly influence the values presented by the server.
        This kind of direct access will also bypass the report
        notification mechanism (i.e. changes will not cause a report!).
        Therefore this function should be used with care. It could be
        useful to access arrays of DataObjects.

        Parameters
        ----------
        data_object : DataObject
            Data object to specify the FCD
        fc : FunctionalConstraint
            Functional constraint to specify the FCD

        Returns
        -------
        MmsValue | None
            MmsValue object of the MMS Named Variable or None if the value does not exist.
        """
        handle = Wrapper.lib.IedServer_getFunctionalConstrainedData(
            self._handle,
            data_object.handle,
            fc.value,
        )
        if handle:
            return MmsValue(handle)
        return None

    def get_boolean(self, data_attribute: DataAttribute) -> bool:
        """Get data attribute value of a boolean data attribute.

        If data attribute is not a boolean, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        bool
            Value of the attribute
        """
        return Wrapper.lib.IedServer_getBooleanAttributeValue(self._handle, data_attribute.handle)

    def get_int32(self, data_attribute: DataAttribute) -> int:
        """Get data attribute value of an int32 data attribute.

        If data attribute is not an int32, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        int
            Value of the attribute
        """
        return Wrapper.lib.IedServer_getInt32AttributeValue(self._handle, data_attribute.handle)

    def get_int64(self, data_attribute: DataAttribute) -> int:
        """Get data attribute value of an int64 data attribute.

        If data attribute is not an int64, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        int
            Value of the attribute
        """
        return Wrapper.lib.IedServer_getInt64AttributeValue(self._handle, data_attribute.handle)

    def get_uint32(self, data_attribute: DataAttribute) -> int:
        """Get data attribute value of an uint32 data attribute.

        If data attribute is not an uint32, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        int
            Value of the attribute
        """
        return Wrapper.lib.IedServer_getUInt32AttributeValue(self._handle, data_attribute.handle)

    def get_float(self, data_attribute: DataAttribute) -> float:
        """Get data attribute value of a float data attribute.

        If data attribute is not a float, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        float
            Value of the attribute
        """
        return Wrapper.lib.IedServer_getFloatAttributeValue(self._handle, data_attribute.handle)

    def get_utc_time(self, data_attribute: DataAttribute) -> datetime.datetime:
        """Get data attribute value of an UTC time data attribute.

        If data attribute is not an UTC time, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        datetime.datetime
            Value of the attribute
        """
        value = Wrapper.lib.IedServer_getUTCTimeAttributeValue(self._handle, data_attribute.handle)
        return convert_to_datetime(value)

    def get_bit_string(self, data_attribute: DataAttribute) -> int:
        """Get data attribute value of a bit string data attribute.

        If data attribute is not a bit string, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        int
            Value of the attribute
        """
        return Wrapper.lib.IedServer_getBitStringAttributeValue(
            self._handle, data_attribute.handle
        )

    def get_string(self, data_attribute: DataAttribute) -> bytes:
        """Get data attribute value of a string data attribute.

        If data attribute is not a string, the behavior of the return
        value is unpredictible.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute

        Returns
        -------
        bytes
            Value of the attribute
        """
        return Wrapper.lib.IedServer_getStringAttributeValue(self._handle, data_attribute.handle)

    def update_value(self, data_attribute: DataAttribute, value: MmsValue):
        """Update the MmsValue object of an IEC 61850 data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : MmsValue
            MmsValue object used to update the value cached by the server.
        """
        Wrapper.lib.IedServer_updateAttributeValue(
            self._handle,
            data_attribute.handle,
            value.handle,
        )

    def update_float(self, data_attribute: DataAttribute, value: float):
        """Update the value of an IEC 61850 float data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : float
            New float value of the data attribute.
        """
        Wrapper.lib.IedServer_updateFloatAttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_int32(self, data_attribute: DataAttribute, value: int):
        """Update the value of an IEC 61850 int32 data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : int
            New int32 value of the data attribute.
        """
        Wrapper.lib.IedServer_updateInt32AttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_dbpos(self, data_attribute: DataAttribute, value: Dbpos):
        """Update the value of an IEC 61850 Dbpos (double point/position) data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : Dbpos
            New Dbpos (double point/position) value of the data attribute.
        """
        Wrapper.lib.IedServer_updateDbposValue(
            self._handle,
            data_attribute.handle,
            value.value,
        )

    def update_int64(self, data_attribute: DataAttribute, value: int):
        """Update the value of an IEC 61850 int64 data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : int
            New int64 value of the data attribute.
        """
        Wrapper.lib.IedServer_updateInt64AttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_uint(
        self,
        data_attribute: DataAttribute,
        value: int,
    ):
        """Update the value of an IEC 61850 uint data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : int
            New uint value of the data attribute.
        """
        Wrapper.lib.IedServer_updateUnsignedAttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_bit_string(
        self,
        data_attribute: DataAttribute,
        value: int,
    ):
        """Update the value of an IEC 61850 bit string data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : int
            New bit string value of the data attribute.
        """
        Wrapper.lib.IedServer_updateBitStringAttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_boolean(
        self,
        data_attribute: DataAttribute,
        value: bool,
    ):
        """Update the value of an IEC 61850 boolean data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : bool
            New boolean value of the data attribute.
        """
        Wrapper.lib.IedServer_updateBooleanAttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_string(
        self,
        data_attribute: DataAttribute,
        value: str | bytes,
    ):
        """Update the value of an IEC 61850 string data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : str | bytes
            New string value of the data attribute.
        """
        value = convert_to_bytes(value)
        Wrapper.lib.IedServer_updateVisibleStringAttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_utc_time(
        self,
        data_attribute: DataAttribute,
        value: datetime.datetime = datetime.datetime.now().astimezone(),
    ):
        """Update the value of an IEC 61850 UTC time data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : datetime.datetime, optional
            New UTC time value of the data attribute, by default
            datetime.datetime.now().astimezone()
        """
        val_uint64 = convert_to_uint64(value)
        Wrapper.lib.IedServer_updateUTCTimeAttributeValue(
            self._handle,
            data_attribute.handle,
            val_uint64,
        )

    def update_timestamp(
        self,
        data_attribute: DataAttribute,
        value: Timestamp,
    ):
        """Update the value of an IEC 61850 Timestamp data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : Timestamp
            New Timestamp value of the data attribute.
        """
        Wrapper.lib.IedServer_updateTimestampAttributeValue(
            self._handle,
            data_attribute.handle,
            value,
        )

    def update_quality(self, data_attribute: DataAttribute, value: Quality):
        """Update the value of an IEC 61850 quality data attribute.

        This function will also check if a trigger condition is satisfied in the case when a report
        or GOOSE control block is enabled.

        Parameters
        ----------
        data_attribute : DataAttribute
            Data attribute
        value : Quality
            New quality value of the data attribute.
        """
        Wrapper.lib.IedServer_updateQuality(
            self._handle,
            data_attribute.handle,
            value,
        )

    def lock_data_model(self):
        """Lock the data model for data update.

        This function should be called before the data model is updated.
        After updating the data model the function
        ``IedServer_unlockDataModel`` should be called. Client requests
        will be postponed until the lock is removed.

        See Also
        --------
        unlock_data_model

        Notes
        -----
        This method should never be called inside of a callback function.
        In the context of a library callback the data model is always
        already locked! Calling this function inside of a library callback
        may lead to a deadlock condition.
        """
        Wrapper.lib.IedServer_lockDataModel(self._handle)

    def unlock_data_model(self):
        """Unlock the data model and process pending client requests.

        See Also
        --------
        lock_data_model

        Notes
        -----
        This method should never be called inside of a callback function.
        In the context of a library callback the data model is always
        already locked!
        """
        Wrapper.lib.IedServer_unlockDataModel(self._handle)

    def set_default_write_policy(
        self,
        fc: Literal[
            FunctionalConstraint.DC,
            FunctionalConstraint.CF,
            FunctionalConstraint.SP,
            FunctionalConstraint.SV,
            FunctionalConstraint.SE,
        ],
        policy: AccessPolicy,
    ):
        """Change the default write access policy for a specific functionnal constraint.

        Parameters
        ----------
        fc : FunctionalConstraint
            FC for which to change the default write access policy. Only
            DC, CF, SP, SV and SE are supported
        policy : AccessPolicy
            New policy to apply.
        """
        Wrapper.lib.IedServer_setWriteAccessPolicy(self._handle, fc.value, policy.value)

    def set_filestore_basepath(self, basepath: str | bytes):
        """Set the virtual filestore basepath for the file services.

        Parameters
        ----------
        basepath : str | bytes
            Local path to the base folder for file service
        """
        basepath = convert_to_bytes(basepath)
        Wrapper.lib.IedServer_setFilestoreBasepath(
            self._handle,  # IedServer self
            basepath,  # const char* basepath
        )
