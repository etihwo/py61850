"""Module for C binding with iec61850/inc/iec61850_server.h"""

from ctypes import (
    CDLL,
    CFUNCTYPE,
    POINTER,
    Structure,
    c_bool,
    c_char_p,
    c_float,
    c_int,
    c_int32,
    c_int64,
    c_uint,
    c_uint8,
    c_uint32,
    c_uint64,
    c_void_p,
)

from ..mms import MmsDataAccessError, MmsServer, MmsValue
from ..mms.iso_connection_parameters import AcseAuthenticator
from .iec61850_common import (
    ACSIClass,
    ControlAddCause,
    ControlLastApplError,
    ControlModel,
    Dbpos,
    FunctionalConstraint,
    Quality,
    Timestamp,
)
from .model import (
    DataAttribute,
    DataObject,
    DataSet,
    IedModel,
    LogicalDevice,
    LogicalNode,
    ReportControlBlock,
    SettingGroupControlBlock,
    SVControlBlock,
)


class sClientConnection(Structure): ...


TLSConfiguration = c_void_p  # TODO : to be moved in the right file
LogStorage = c_void_p  # TODO : to be moved in the right file

IedServerConfig = c_void_p
IedServer = c_void_p
ClientConnection = c_void_p
ControlAction = c_void_p
MmsGooseControlBlock = c_void_p

CheckHandlerResult = c_int
ControlHandlerResult = c_int
SelectStateChangedReason = c_int
IedServer_RCBEventType = c_int
AccessPolicy = c_int
IedServer_DataSetOperation = c_int
IedServer_DirectoryCategory = c_int
IedServer_ControlBlockAccessType = c_int

IedConnectionIndicationHandler = CFUNCTYPE(
    None,  # return type: void
    IedServer,  # IedServer self,
    ClientConnection,  #  ClientConnection connection,
    c_bool,  # bool connected,
    c_void_p,  #  void* parameter
)

ActiveSettingGroupChangedHandler = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter,
    POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb,
    c_uint8,  # uint8_t newActSg,
    ClientConnection,  #  ClientConnection connection
)

EditSettingGroupChangedHandler = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter,
    POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb,
    c_uint8,  # uint8_t newEditSg,
    ClientConnection,  #  ClientConnection connection
)

EditSettingGroupConfirmationHandler = CFUNCTYPE(
    None,  # return type: void
    c_void_p,  # void* parameter,
    POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb,
    c_uint8,  # uint8_t editSg,
)

ControlPerformCheckHandler = CFUNCTYPE(
    CheckHandlerResult,  # return type: CheckHandlerResult
    ControlAction,  # ControlAction action,
    c_void_p,  #  void* parameter,
    POINTER(MmsValue),  # MmsValue* ctlVal
    c_bool,  # bool test
    c_bool,  # bool interlockCheck
)

ControlWaitForExecutionHandler = CFUNCTYPE(
    ControlHandlerResult,  # return type: ControlHandlerResult
    ControlAction,  # ControlAction action
    c_void_p,  #  void* parameter,
    POINTER(MmsValue),  # MmsValue* ctlVal
    c_bool,  # bool test
    c_bool,  # bool synchroCheck
)

ControlHandler = CFUNCTYPE(
    ControlHandlerResult,  # return type: ControlHandlerResult
    ControlAction,  # ControlAction action
    c_void_p,  #  void* parameter,
    POINTER(MmsValue),  # MmsValue* ctlVal
    c_bool,  # bool test
)


ControlSelectStateChangedHandler = CFUNCTYPE(
    None,  # return type: void
    ControlAction,  # ControlAction action
    c_void_p,  #  void* parameter,
    c_bool,  # bool isSelected,
    SelectStateChangedReason,  # SelectStateChangedReason reason
)
IedServer_RCBEventHandler = CFUNCTYPE(
    None,  # return type: void
    c_void_p,  # void* parameter
    POINTER(ReportControlBlock),  # ReportControlBlock* rcb,
    ClientConnection,  # ClientConnection connection,
    IedServer_RCBEventType,  #  IedServer_RCBEventType event,
    c_char_p,  #  const char* parameterName,
    MmsDataAccessError,  #  MmsDataAccessError serviceError
)


SVCBEventHandler = CFUNCTYPE(
    None,  # return type: void
    POINTER(SVControlBlock),  # SVControlBlock* svcb
    c_int,  # int event,
    c_void_p,  # void* parameter
)

GoCBEventHandler = CFUNCTYPE(
    None,  # return type: void
    MmsGooseControlBlock,  # MmsGooseControlBlock goCb
    c_int,  # int event,
    c_void_p,  # void* parameter
)

WriteAccessHandler = CFUNCTYPE(
    MmsDataAccessError,  # return type: MmsDataAccessError
    POINTER(DataAttribute),  # DataAttribute* dataAttribute
    POINTER(MmsValue),  # MmsValue* value,
    ClientConnection,  #  ClientConnection connection,
    c_void_p,  # void* parameter
)

ReadAccessHandler = CFUNCTYPE(
    MmsDataAccessError,  # return type: MmsDataAccessError
    POINTER(LogicalDevice),  # LogicalDevice* ld
    POINTER(LogicalNode),  # LogicalNode* ln,
    POINTER(DataObject),  # DataObject* dataObject,
    FunctionalConstraint,  # FunctionalConstraint fc,
    ClientConnection,  #  ClientConnection connection,
    c_void_p,  # void* parameter
)

IedServer_DataSetAccessHandler = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter
    ClientConnection,  # ClientConnection connection,
    IedServer_DataSetOperation,  #  IedServer_DataSetOperation operation,
    c_char_p,  #  const char* datasetRef
)

IedServer_DirectoryAccessHandler = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter,
    ClientConnection,  # ClientConnection connection,
    IedServer_DirectoryCategory,  #  IedServer_DirectoryCategory category,
    POINTER(LogicalDevice),  #  LogicalDevice* logicalDevice
)

IedServer_ListObjectsAccessHandler = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter
    ClientConnection,  # ClientConnection connection,
    ACSIClass,  # ACSIClass acsiClass,
    POINTER(LogicalDevice),  # LogicalDevice* ld
    POINTER(LogicalNode),  # LogicalNode* ln,
    c_char_p,  # const char* objectName,
    c_char_p,  # const char* subObjectName,
    FunctionalConstraint,  #  FunctionalConstraint fc
)

IedServer_ControlBlockAccessHandler = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter
    ClientConnection,  # ClientConnection connection,
    ACSIClass,  #  ACSIClass acsiClass,
    POINTER(LogicalDevice),  # LogicalDevice* ld
    POINTER(LogicalNode),  # LogicalNode* ln,
    c_char_p,  # const char* objectName,
    c_char_p,  # const char* subObjectName,
    IedServer_ControlBlockAccessType,  # IedServer_ControlBlockAccessType accessType
)


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    lib.IedServerConfig_create.argtypes = []
    lib.IedServerConfig_create.restype = IedServerConfig

    lib.IedServerConfig_destroy.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_destroy.restype = None

    lib.IedServerConfig_setEdition.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_uint8,  # uint8_t edition
    ]
    lib.IedServerConfig_setEdition.restype = None

    lib.IedServerConfig_getEdition.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getEdition.restype = c_uint8

    lib.IedServerConfig_setReportBufferSize.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_int,  # int reportBufferSize
    ]
    lib.IedServerConfig_setReportBufferSize.restype = None

    lib.IedServerConfig_getReportBufferSize.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getReportBufferSize.restype = c_int

    lib.IedServerConfig_setReportBufferSizeForURCBs.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_int,  # int reportBufferSize
    ]
    lib.IedServerConfig_setReportBufferSizeForURCBs.restype = None

    lib.IedServerConfig_getReportBufferSizeForURCBs.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getReportBufferSizeForURCBs.restype = c_int

    lib.IedServerConfig_setMaxMmsConnections.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_int,  # int maxConnections
    ]
    lib.IedServerConfig_setMaxMmsConnections.restype = None

    lib.IedServerConfig_getMaxMmsConnections.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getMaxMmsConnections.restype = c_int

    lib.IedServerConfig_setSyncIntegrityReportTimes.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_setSyncIntegrityReportTimes.restype = None

    lib.IedServerConfig_getSyncIntegrityReportTimes.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getSyncIntegrityReportTimes.restype = c_bool

    lib.IedServerConfig_setFileServiceBasePath.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_char_p,  # const char* basepath
    ]
    lib.IedServerConfig_setFileServiceBasePath.restype = None

    lib.IedServerConfig_getFileServiceBasePath.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getFileServiceBasePath.restype = c_char_p

    lib.IedServerConfig_enableFileService.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_enableFileService.restype = None

    lib.IedServerConfig_isFileServiceEnabled.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_isFileServiceEnabled.restype = c_bool

    lib.IedServerConfig_enableDynamicDataSetService.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_enableDynamicDataSetService.restype = None

    lib.IedServerConfig_isDynamicDataSetServiceEnabled.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_isDynamicDataSetServiceEnabled.restype = c_bool

    lib.IedServerConfig_setMaxAssociationSpecificDataSets.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_int,  # int maxDataSets
    ]
    lib.IedServerConfig_setMaxAssociationSpecificDataSets.restype = None

    lib.IedServerConfig_getMaxAssociationSpecificDataSets.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getMaxAssociationSpecificDataSets.restype = c_int

    lib.IedServerConfig_setMaxDomainSpecificDataSets.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_int,  # int maxDataSets
    ]
    lib.IedServerConfig_setMaxDomainSpecificDataSets.restype = None

    lib.IedServerConfig_getMaxDomainSpecificDataSets.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getMaxDomainSpecificDataSets.restype = c_int

    lib.IedServerConfig_setMaxDataSetEntries.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_int,  # int maxDataSetEntries
    ]
    lib.IedServerConfig_setMaxDataSetEntries.restype = None

    lib.IedServerConfig_getMaxDatasSetEntries.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_getMaxDatasSetEntries.restype = c_int

    lib.IedServerConfig_enableLogService.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_enableLogService.restype = None

    lib.IedServerConfig_enableEditSG.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_enableEditSG.restype = None

    lib.IedServerConfig_enableResvTmsForSGCB.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_enableResvTmsForSGCB.restype = None

    lib.IedServerConfig_enableResvTmsForBRCB.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_enableResvTmsForBRCB.restype = None

    lib.IedServerConfig_isResvTmsForBRCBEnabled.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_isResvTmsForBRCBEnabled.restype = c_bool

    lib.IedServerConfig_enableOwnerForRCB.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_enableOwnerForRCB.restype = None

    lib.IedServerConfig_isOwnerForRCBEnabled.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_isOwnerForRCBEnabled.restype = c_bool

    lib.IedServerConfig_useIntegratedGoosePublisher.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_bool,  # bool enable
    ]
    lib.IedServerConfig_useIntegratedGoosePublisher.restype = None

    lib.IedServerConfig_isLogServiceEnabled.argtypes = [
        IedServerConfig,  # IedServerConfig self
    ]
    lib.IedServerConfig_isLogServiceEnabled.restype = c_bool

    lib.IedServerConfig_setReportSetting.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_uint8,  # uint8_t setting
        c_bool,  # bool isDyn
    ]
    lib.IedServerConfig_setReportSetting.restype = None

    lib.IedServerConfig_getReportSetting.argtypes = [
        IedServerConfig,  # IedServerConfig self
        c_uint8,  # uint8_t setting
    ]
    lib.IedServerConfig_getReportSetting.restype = c_bool

    lib.IedServer_create.argtypes = [
        POINTER(IedModel),  # IedModel* dataModel
    ]
    lib.IedServer_create.restype = IedServer

    lib.IedServer_createWithTlsSupport.argtypes = [
        POINTER(IedModel),  # IedModel* dataModel
        TLSConfiguration,  # TLSConfiguration tlsConfiguration
    ]
    lib.IedServer_createWithTlsSupport.restype = IedServer

    lib.IedServer_createWithConfig.argtypes = [
        POINTER(IedModel),  # IedModel* dataModel
        TLSConfiguration,  # TLSConfiguration tlsConfiguration
        IedServerConfig,  # IedServerConfig serverConfiguration
    ]
    lib.IedServer_createWithConfig.restype = IedServer

    lib.IedServer_destroy.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_destroy.restype = None

    lib.IedServer_addAccessPoint.argtypes = [
        IedServer,  # IedServer self
        c_char_p,  # const char* ipAddr
        c_int,  # int tcpPort
        TLSConfiguration,  # TLSConfiguration tlsConfiguration
    ]
    lib.IedServer_addAccessPoint.restype = c_bool

    lib.IedServer_setLocalIpAddress.argtypes = [
        IedServer,  # IedServer self
        c_char_p,  # const char* localIpAddress
    ]
    lib.IedServer_setLocalIpAddress.restype = None

    lib.IedServer_setServerIdentity.argtypes = [
        IedServer,  # IedServer self
        c_char_p,  # const char* vendor
        c_char_p,  # const char* model
        c_char_p,  # const char* revision
    ]
    lib.IedServer_setServerIdentity.restype = None

    lib.IedServer_setFilestoreBasepath.argtypes = [
        IedServer,  # IedServer self
        c_char_p,  # const char* basepath
    ]
    lib.IedServer_setFilestoreBasepath.restype = None

    lib.IedServer_setLogStorage.argtypes = [
        IedServer,  # IedServer self
        c_char_p,  # const char* logRef
        LogStorage,  # LogStorage logStorage
    ]
    lib.IedServer_setLogStorage.restype = None

    lib.IedServer_start.argtypes = [
        IedServer,  # IedServer self
        c_int,  # int tcpPort
    ]
    lib.IedServer_start.restype = None

    lib.IedServer_stop.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_stop.restype = None

    lib.IedServer_startThreadless.argtypes = [
        IedServer,  # IedServer self
        c_int,  # int tcpPort
    ]
    lib.IedServer_startThreadless.restype = None

    lib.IedServer_waitReady.argtypes = [
        IedServer,  # IedServer self
        c_uint,  # unsigned int timeoutMs
    ]
    lib.IedServer_waitReady.restype = c_int

    lib.IedServer_processIncomingData.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_processIncomingData.restype = None

    lib.IedServer_performPeriodicTasks.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_performPeriodicTasks.restype = None

    lib.IedServer_stopThreadless.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_stopThreadless.restype = None

    lib.IedServer_getDataModel.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_getDataModel.restype = POINTER(IedModel)

    lib.IedServer_isRunning.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_isRunning.restype = c_bool

    lib.IedServer_getNumberOfOpenConnections.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_getNumberOfOpenConnections.restype = c_int

    lib.IedServer_getMmsServer.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_getMmsServer.restype = MmsServer

    lib.IedServer_enableGoosePublishing.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_enableGoosePublishing.restype = None

    lib.IedServer_disableGoosePublishing.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_disableGoosePublishing.restype = None

    lib.IedServer_setGooseInterfaceId.argtypes = [
        IedServer,  # IedServer self
        c_char_p,  # const char* interfaceId
    ]
    lib.IedServer_setGooseInterfaceId.restype = None

    lib.IedServer_setGooseInterfaceIdEx.argtypes = [
        IedServer,  # IedServer self
        POINTER(LogicalNode),  # LogicalNode* ln,
        c_char_p,  #  const char* gcbName
        c_char_p,  # const char* interfaceId
    ]
    lib.IedServer_setGooseInterfaceIdEx.restype = None

    lib.IedServer_useGooseVlanTag.argtypes = [
        IedServer,  # IedServer self
        POINTER(LogicalNode),  # LogicalNode* ln,
        c_char_p,  #  const char* gcbName
        c_bool,  # bool useVlanTag
    ]
    lib.IedServer_useGooseVlanTag.restype = None

    lib.IedServer_setTimeQuality.argtypes = [
        IedServer,  # IedServer self
        c_bool,  # bool leapSecondKnown,
        c_bool,  #  bool clockFailure,
        c_bool,  # bool clockNotSynchronized,
        c_int,  # int subsecondPrecision
    ]
    lib.IedServer_setTimeQuality.restype = None

    lib.IedServer_setAuthenticator.argtypes = [
        IedServer,  # IedServer self
        AcseAuthenticator,  # AcseAuthenticator authenticator,
        c_void_p,  # void* authenticatorParameter
    ]
    lib.IedServer_setAuthenticator.restype = None

    lib.ClientConnection_getPeerAddress.argtypes = [
        ClientConnection,  # ClientConnection self
    ]
    lib.ClientConnection_getPeerAddress.restype = c_char_p

    lib.ClientConnection_getLocalAddress.argtypes = [
        ClientConnection,  # ClientConnection self
    ]
    lib.ClientConnection_getLocalAddress.restype = c_char_p

    lib.ClientConnection_getSecurityToken.argtypes = [
        ClientConnection,  # ClientConnection self
    ]
    lib.ClientConnection_getSecurityToken.restype = c_void_p

    lib.ClientConnection_abort.argtypes = [
        ClientConnection,  # ClientConnection self
    ]
    lib.ClientConnection_abort.restype = c_bool

    lib.ClientConnection_claimOwnership.argtypes = [
        ClientConnection,  # ClientConnection self
    ]
    lib.ClientConnection_claimOwnership.restype = ClientConnection

    lib.ClientConnection_release.argtypes = [
        ClientConnection,  # ClientConnection self
    ]
    lib.ClientConnection_release.restype = None

    lib.IedServer_setConnectionIndicationHandler.argtypes = [
        IedServer,  # IedServer self
        IedConnectionIndicationHandler,  # IedConnectionIndicationHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setConnectionIndicationHandler.restype = None

    lib.IedServer_lockDataModel.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_lockDataModel.restype = None

    lib.IedServer_unlockDataModel.argtypes = [
        IedServer,  # IedServer self
    ]
    lib.IedServer_unlockDataModel.restype = None

    lib.IedServer_getAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute
    ]
    lib.IedServer_getAttributeValue.restype = POINTER(MmsValue)

    lib.IedServer_getBooleanAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getBooleanAttributeValue.restype = c_bool

    lib.IedServer_getInt32AttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getInt32AttributeValue.restype = c_int32

    lib.IedServer_getInt64AttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getInt64AttributeValue.restype = c_int64

    lib.IedServer_getUInt32AttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getUInt32AttributeValue.restype = c_uint32

    lib.IedServer_getFloatAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getFloatAttributeValue.restype = c_float

    lib.IedServer_getUTCTimeAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getUTCTimeAttributeValue.restype = c_uint64

    lib.IedServer_getBitStringAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getBitStringAttributeValue.restype = c_uint32

    lib.IedServer_getStringAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  const DataAttribute* dataAttribute
    ]
    lib.IedServer_getStringAttributeValue.restype = c_char_p

    lib.IedServer_getFunctionalConstrainedData.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataObject),  #  DataObject* dataObject
        FunctionalConstraint,  #  FunctionalConstraint fc
    ]
    lib.IedServer_getFunctionalConstrainedData.restype = POINTER(MmsValue)

    lib.IedServer_updateAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        POINTER(MmsValue),  #  MmsValue* value
    ]
    lib.IedServer_updateAttributeValue.restype = None

    lib.IedServer_updateFloatAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_float,  # float value
    ]
    lib.IedServer_updateFloatAttributeValue.restype = None

    lib.IedServer_updateInt32AttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_int32,  # int32_t value
    ]
    lib.IedServer_updateInt32AttributeValue.restype = None

    lib.IedServer_updateDbposValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        Dbpos,  # Dbpos value
    ]
    lib.IedServer_updateDbposValue.restype = None

    lib.IedServer_updateInt64AttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_int64,  # int64_t value
    ]
    lib.IedServer_updateInt64AttributeValue.restype = None

    lib.IedServer_updateUnsignedAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_uint32,  # uint32_t value
    ]
    lib.IedServer_updateUnsignedAttributeValue.restype = None

    lib.IedServer_updateBitStringAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_uint32,  # uint32_t value
    ]
    lib.IedServer_updateBitStringAttributeValue.restype = None

    lib.IedServer_updateBooleanAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_bool,  # bool value
    ]
    lib.IedServer_updateBooleanAttributeValue.restype = None

    lib.IedServer_updateVisibleStringAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_char_p,  # char *value
    ]
    lib.IedServer_updateVisibleStringAttributeValue.restype = None

    lib.IedServer_updateUTCTimeAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        c_uint64,  # uint64_t *value
    ]
    lib.IedServer_updateUTCTimeAttributeValue.restype = None

    lib.IedServer_updateTimestampAttributeValue.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        POINTER(Timestamp),  # Timestamp* timestamp
    ]
    lib.IedServer_updateTimestampAttributeValue.restype = None

    lib.IedServer_updateQuality.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataAttribute),  #  DataAttribute* dataAttribute,
        Quality,  # Quality quality
    ]
    lib.IedServer_updateQuality.restype = None

    lib.IedServer_changeActiveSettingGroup.argtypes = [
        IedServer,  # IedServer self
        POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb,
        c_uint8,  # uint8_t newActiveSg
    ]
    lib.IedServer_changeActiveSettingGroup.restype = None

    lib.IedServer_getActiveSettingGroup.argtypes = [
        IedServer,  # IedServer self
        POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb,
    ]
    lib.IedServer_getActiveSettingGroup.restype = c_uint8

    lib.IedServer_setActiveSettingGroupChangedHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb
        ActiveSettingGroupChangedHandler,  # ActiveSettingGroupChangedHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setActiveSettingGroupChangedHandler.restype = None

    lib.IedServer_setEditSettingGroupChangedHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb
        EditSettingGroupChangedHandler,  # EditSettingGroupChangedHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setEditSettingGroupChangedHandler.restype = None

    lib.IedServer_setEditSettingGroupConfirmationHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(SettingGroupControlBlock),  #  SettingGroupControlBlock* sgcb
        EditSettingGroupConfirmationHandler,  # EditSettingGroupConfirmationHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setEditSettingGroupConfirmationHandler.restype = None

    lib.ControlAction_setError.argtypes = [
        ControlAction,  # ControlAction self
        ControlLastApplError,  # ControlLastApplError error
    ]
    lib.ControlAction_setError.restype = None

    lib.ControlAction_setAddCause.argtypes = [
        ControlAction,  # ControlAction self
        ControlAddCause,  # ControlAddCause addCause
    ]
    lib.ControlAction_setAddCause.restype = None

    lib.ControlAction_getOrCat.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getOrCat.restype = c_int

    lib.ControlAction_getOrIdent.argtypes = [
        ControlAction,  # ControlAction self
        POINTER(c_int),  # int* orIdentSize
    ]
    lib.ControlAction_getOrIdent.restype = POINTER(c_uint8)

    lib.ControlAction_getCtlNum.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getCtlNum.restype = c_int

    lib.ControlAction_getSynchroCheck.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getSynchroCheck.restype = c_bool

    lib.ControlAction_getInterlockCheck.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getInterlockCheck.restype = c_bool

    lib.ControlAction_isSelect.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_isSelect.restype = c_bool

    lib.ControlAction_getClientConnection.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getClientConnection.restype = ClientConnection

    lib.ControlAction_getControlObject.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getControlObject.restype = POINTER(DataObject)

    lib.ControlAction_getControlTime.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getControlTime.restype = c_uint64

    lib.ControlAction_getT.argtypes = [
        ControlAction,  # ControlAction self
    ]
    lib.ControlAction_getT.restype = POINTER(Timestamp)

    lib.IedServer_setControlHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataObject),  # DataObject* node,
        ControlHandler,  # ControlHandler handler,
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setControlHandler.restype = None

    lib.IedServer_setPerformCheckHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataObject),  # DataObject* node,
        ControlPerformCheckHandler,  # ControlPerformCheckHandler handler,
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setPerformCheckHandler.restype = None

    lib.IedServer_setWaitForExecutionHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataObject),  # DataObject* node,
        ControlWaitForExecutionHandler,  # ControlWaitForExecutionHandler handler,
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setWaitForExecutionHandler.restype = None

    lib.IedServer_setSelectStateChangedHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataObject),  # DataObject* node,
        ControlSelectStateChangedHandler,  # ControlSelectStateChangedHandler handler,
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setSelectStateChangedHandler.restype = None

    lib.IedServer_updateCtlModel.argtypes = [
        IedServer,  # IedServer self
        POINTER(DataObject),  # DataObject* node,
        ControlModel,  #  ControlModel value
    ]
    lib.IedServer_updateCtlModel.restype = None

    lib.IedServer_setRCBEventHandler.argtypes = [
        IedServer,  # IedServer self
        ControlModel,  #  IedServer_RCBEventHandler handler
        c_void_p,  # void * parameter,
    ]
    lib.IedServer_setRCBEventHandler.restype = None

    lib.IedServer_setSVCBHandler.argtypes = [
        IedServer,  # IedServer self
        POINTER(SVControlBlock),  # SVControlBlock* svcb,
        SVCBEventHandler,  #  SVCBEventHandler handler,
        c_void_p,  #  void* parameter
    ]
    lib.IedServer_setSVCBHandler.restype = None

    lib.IedServer_setGoCBHandler.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
        GoCBEventHandler,  # GoCBEventHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setGoCBHandler.restype = None

    lib.MmsGooseControlBlock_getName.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getName.restype = c_char_p

    lib.MmsGooseControlBlock_getLogicalNode.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getLogicalNode.restype = POINTER(LogicalNode)

    lib.MmsGooseControlBlock_getDataSet.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getDataSet.restype = POINTER(DataSet)

    lib.MmsGooseControlBlock_getGoEna.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getGoEna.restype = c_bool

    lib.MmsGooseControlBlock_getMinTime.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getMinTime.restype = c_int

    lib.MmsGooseControlBlock_getMaxTime.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getMaxTime.restype = c_int

    lib.MmsGooseControlBlock_getFixedOffs.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getFixedOffs.restype = c_bool

    lib.MmsGooseControlBlock_getNdsCom.argtypes = [
        MmsGooseControlBlock,  # MmsGooseControlBlock self
    ]
    lib.MmsGooseControlBlock_getNdsCom.restype = c_bool

    # /***************************************************************************
    #  * Access control
    #  **************************************************************************/

    lib.IedServer_handleWriteAccess.argtypes = [
        IedServer,  # IedServer self,
        POINTER(DataAttribute),  # DataAttribute* dataAttribute,
        WriteAccessHandler,  # WriteAccessHandler handler,
        c_void_p,  #  void* parameter
    ]
    lib.IedServer_handleWriteAccess.restype = None

    lib.IedServer_handleWriteAccessForComplexAttribute.argtypes = [
        IedServer,  # IedServer self,
        POINTER(DataAttribute),  # DataAttribute* dataAttribute,
        WriteAccessHandler,  # WriteAccessHandler handler,
        c_void_p,  #  void* parameter
    ]
    lib.IedServer_handleWriteAccessForComplexAttribute.restype = None

    lib.IedServer_handleWriteAccessForDataObject.argtypes = [
        IedServer,  # IedServer self,
        POINTER(DataObject),  # DataObject* dataObject,
        FunctionalConstraint,  # FunctionalConstraint fc,
        WriteAccessHandler,  # WriteAccessHandler handler,
        c_void_p,  #  void* parameter
    ]
    lib.IedServer_handleWriteAccessForDataObject.restype = None

    lib.IedServer_setWriteAccessPolicy.argtypes = [
        IedServer,  # IedServer self,
        FunctionalConstraint,  #  FunctionalConstraint fc
        AccessPolicy,  # AccessPolicy policy
    ]
    lib.IedServer_setWriteAccessPolicy.restype = None

    lib.IedServer_setReadAccessHandler.argtypes = [
        IedServer,  # IedServer self,
        ReadAccessHandler,  #  ReadAccessHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setReadAccessHandler.restype = None

    lib.IedServer_setDirectoryAccessHandler.argtypes = [
        IedServer,  # IedServer self,
        IedServer_DirectoryAccessHandler,  #  IedServer_DirectoryAccessHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setDirectoryAccessHandler.restype = None

    lib.IedServer_setListObjectsAccessHandler.argtypes = [
        IedServer,  # IedServer self,
        IedServer_ListObjectsAccessHandler,  #  IedServer_ListObjectsAccessHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setListObjectsAccessHandler.restype = None

    lib.IedServer_setControlBlockAccessHandler.argtypes = [
        IedServer,  # IedServer self,
        IedServer_ControlBlockAccessHandler,  #  IedServer_ControlBlockAccessHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedServer_setControlBlockAccessHandler.restype = None

    lib.IedServer_ignoreReadAccess.argtypes = [
        IedServer,  # IedServer self,
        c_bool,  # bool ignore
    ]
    lib.IedServer_ignoreReadAccess.restype = None
