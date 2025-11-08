"""Module for C binding with iec61850/inc/iec61850_client.h"""

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
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_void_p,
)

from ..common.linked_list import LinkedList
from ..mms import MmsType, MmsValue, MmsVariableSpecification
from .iec61850_common import (
    ACSIClass,
    ControlAddCause,
    ControlLastApplError,
    ControlModel,
    FunctionalConstraint,
    PhyComAddress,
    Quality,
    Timestamp,
)


class sClientGooseControlBlock(Structure):
    _fields_ = [
        ("objectReference", c_char_p),
        ("goEna", POINTER(MmsValue)),
        ("goID", POINTER(MmsValue)),
        ("datSet", POINTER(MmsValue)),
        ("confRev", POINTER(MmsValue)),
        ("ndsCom", POINTER(MmsValue)),
        ("dstAddress", POINTER(MmsValue)),
        ("minTime", POINTER(MmsValue)),
        ("maxTime", POINTER(MmsValue)),
        ("fixedOffs", POINTER(MmsValue)),
    ]


class sClientReportControlBlock(Structure):
    _fields_ = [
        ("objectReference", c_char_p),
        ("isBuffered", c_bool),
        ("rptId", POINTER(MmsValue)),
        ("rptEna", POINTER(MmsValue)),
        ("resv", POINTER(MmsValue)),
        ("datSet", POINTER(MmsValue)),
        ("confRev", POINTER(MmsValue)),
        ("optFlds", POINTER(MmsValue)),
        ("bufTm", POINTER(MmsValue)),
        ("sqNum", POINTER(MmsValue)),
        ("trgOps", POINTER(MmsValue)),
        ("intgPd", POINTER(MmsValue)),
        ("gi", POINTER(MmsValue)),
        ("purgeBuf", POINTER(MmsValue)),
        ("entryId", POINTER(MmsValue)),
        ("timeOfEntry", POINTER(MmsValue)),
        ("resvTms", POINTER(MmsValue)),
        ("owner", POINTER(MmsValue)),
    ]


IedConnectionState = c_int


IedClientError = c_int
ReasonForInclusion = c_int
ControlActionType = c_int

IedConnection = c_void_p
ClientDataSet = c_void_p
ClientReport = c_void_p
ClientReportControlBlock = POINTER(sClientReportControlBlock)
ClientGooseControlBlock = POINTER(sClientGooseControlBlock)
ControlObjectClient = c_void_p
FileDirectoryEntry = c_void_p


class LastApplError(Structure):
    _fields_ = [
        ("ctlNum", c_int),
        ("error", ControlLastApplError),
        ("addCause", ControlAddCause),
    ]


ControlObjectClient_ControlActionHandler = CFUNCTYPE(
    None,  # return type: void
    c_uint32,  # uint32_t invokeId,
    c_void_p,  # void* parameter,
    IedClientError,  # IedClientError err,
    ControlActionType,  # ControlActionType type,
    c_bool,  # bool success
)

CommandTerminationHandler = CFUNCTYPE(
    None,  # return type: void
    c_void_p,  # void* parameter,
    ControlObjectClient,  # ControlObjectClient controlClient
)

IedClientGetFileHandler = CFUNCTYPE(
    c_bool,  # return type: c_bool
    c_void_p,  # void* parameter
    POINTER(c_uint8),  #  uint8_t* buffer
    c_uint32,  # uint32_t bytesRead
)

IedConnection_ClosedHandler = CFUNCTYPE(
    None,  # return type: void
    c_void_p,  # parameter
    IedConnection,  # connection
)

IedConnection_FileDirectoryEntryHandler = CFUNCTYPE(
    c_bool,  # return type: c_bool
    c_uint32,  # uint32_t invokeId
    c_void_p,  # void* parameter
    IedClientError,  # IedClientError mmsError
    LinkedList,  # char* filename
    c_uint32,  #  uint32_t size
    c_uint64,  #  uint64_t lastModfified
    c_bool,  #  bool moreFollows
)

IedConnection_GenericServiceHandler = CFUNCTYPE(
    None,  # return type: void
    c_uint32,  # uint32_t invokeId
    c_void_p,  # void* parameter,
    IedClientError,  # IedClientError err
)

IedConnection_GetFileAsyncHandler = CFUNCTYPE(
    c_bool,  # return type: c_bool
    c_uint32,  # uint32_t invokeId
    c_void_p,  #  void* parameter
    IedClientError,  # IedClientError err
    c_uint32,  # uint32_t originalInvokeId
    POINTER(c_uint8),  # uint8_t* buffer
    c_uint32,  # uint32_t bytesRead
    c_bool,  # bool moreFollows
)

IedConnection_GetGoCBValuesHandler = CFUNCTYPE(
    None,  # return type: void
    c_uint32,  # uint32_t invokeId
    c_void_p,  # void* parameter,
    IedClientError,  # IedClientError err
    ClientGooseControlBlock,  # ClientGooseControlBlock goCB
)

IedConnection_GetNameListHandler = CFUNCTYPE(
    None,  # return type: void
    c_uint32,  # uint32_t invokeId
    c_void_p,  # void* parameter
    IedClientError,  # IedClientError err
    LinkedList,  # LinkedList nameList
    c_bool,  # bool moreFollows
)

IedConnection_GetVariableSpecificationHandler = CFUNCTYPE(
    None,  # return type: void
    c_uint32,  # uint32_t invokeId
    c_void_p,  # void* parameter
    IedClientError,  # IedClientError err
    MmsVariableSpecification,  # MmsVariableSpecification* spec
)

IedConnection_QueryLogHandler = CFUNCTYPE(
    None,  # return type: void
    c_uint32,  # uint32_t invokeId
    c_void_p,  # void* parameter
    IedClientError,  # , IedClientError mmsError
    LinkedList,  # LinkedList /* <MmsJournalEntry> */ journalEntries
    c_bool,  #  bool moreFollows
)

IedConnection_ReadObjectHandler = CFUNCTYPE(
    None,  # return type: void
    c_uint32,  # uint32_t invokeId
    c_void_p,  #  void* parameter
    IedClientError,  # IedClientError err
    POINTER(MmsValue),  # MmsValue* value
)

IedConnection_StateChangedHandler = CFUNCTYPE(
    None,  # return type: void
    c_void_p,  # parameter
    IedConnection,  # connection
    IedConnectionState,  # newState
)

ReportCallbackFunction = CFUNCTYPE(
    None,  # return type: void
    c_void_p,  # parameter
    ClientReport,  # report
)


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""
    ####################################################
    # Connection creation and destruction
    ####################################################

    lib.IedConnection_create.argtypes = []
    lib.IedConnection_create.restype = IedConnection

    lib.IedConnection_destroy.argtypes = [IedConnection]
    lib.IedConnection_destroy.restype = None

    lib.IedConnection_destroy.argtypes = [IedConnection]
    lib.IedConnection_destroy.restype = None

    lib.IedConnection_setLocalAddress.argtypes = [
        IedConnection,  # IedConnection self
        c_char_p,  # const char* localIpAddress
        c_int,  # int localPort
    ]
    lib.IedConnection_setLocalAddress.restype = None

    lib.IedConnection_setConnectTimeout.argtypes = [
        IedConnection,  # IedConnection self
        c_uint32,  # uint32_t timeoutInMs
    ]
    lib.IedConnection_setConnectTimeout.restype = None

    lib.IedConnection_setMaxOutstandingCalls.argtypes = [
        IedConnection,  # IedConnection self
        c_int,  # int calling
        c_int,  # int called
    ]
    lib.IedConnection_setMaxOutstandingCalls.restype = None

    lib.IedConnection_setRequestTimeout.argtypes = [
        IedConnection,  # IedConnection self
        c_uint32,  # uint32_t timeoutInMs
    ]
    lib.IedConnection_setRequestTimeout.restype = None

    lib.IedConnection_getRequestTimeout.argtypes = [IedConnection]
    lib.IedConnection_getRequestTimeout.restype = c_uint32

    lib.IedConnection_setTimeQuality.argtypes = [
        IedConnection,  # IedConnection self
        c_bool,  # bool leapSecondKnown
        c_bool,  # bool clockFailure
        c_bool,  # bool clockNotSynchronized
        c_int,  # int subsecondPrecision
    ]
    lib.IedConnection_setTimeQuality.restype = None

    lib.IedConnection_tick.argtypes = [IedConnection]
    lib.IedConnection_tick.restype = c_bool

    ####################################################
    # Association service
    ####################################################

    lib.IedConnection_connect.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
        c_int,
    ]
    lib.IedConnection_connect.restype = None

    lib.IedConnection_abort.argtypes = [
        IedConnection,
        POINTER(IedClientError),
    ]
    lib.IedConnection_abort.restype = None

    lib.IedConnection_release.argtypes = [
        IedConnection,
        POINTER(IedClientError),
    ]
    lib.IedConnection_release.restype = None

    lib.IedConnection_close.argtypes = [IedConnection]
    lib.IedConnection_close.restype = None

    lib.IedConnection_getState.argtypes = [IedConnection]
    lib.IedConnection_getState.restype = IedConnectionState

    lib.IedConnection_getLastApplError.argtypes = [IedConnection]
    lib.IedConnection_getLastApplError.restype = LastApplError

    lib.IedConnection_installConnectionClosedHandler.argtypes = [
        IedConnection,  # IedConnection self
        IedConnection_ClosedHandler,  # IedConnectionClosedHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_installConnectionClosedHandler.restype = None

    lib.IedConnection_installStateChangedHandler.argtypes = [
        IedConnection,  # IedConnection self
        IedConnection_StateChangedHandler,  # IedConnection_StateChangedHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_installStateChangedHandler.restype = None

    ####################################################
    # GOOSE services handling (MMS part)
    ####################################################

    ####################################################
    # ClientGooseControlBlock class
    ####################################################

    lib.ClientGooseControlBlock_create.argtypes = [
        c_char_p,  # const char* dataAttributeReference
    ]
    lib.ClientGooseControlBlock_create.restype = ClientGooseControlBlock

    lib.ClientGooseControlBlock_destroy.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_destroy.restype = None

    lib.ClientGooseControlBlock_getGoEna.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getGoEna.restype = c_bool

    lib.ClientGooseControlBlock_setGoEna.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
        c_bool,  # bool goEna
    ]
    lib.ClientGooseControlBlock_setGoEna.restype = None

    lib.ClientGooseControlBlock_getGoID.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getGoID.restype = c_char_p

    lib.ClientGooseControlBlock_setGoID.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
        c_char_p,  # const char* goID
    ]
    lib.ClientGooseControlBlock_setGoID.restype = None

    lib.ClientGooseControlBlock_getDatSet.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getDatSet.restype = c_char_p

    lib.ClientGooseControlBlock_setDatSet.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
        c_char_p,  # const char* datSet
    ]
    lib.ClientGooseControlBlock_setDatSet.restype = None

    lib.ClientGooseControlBlock_getConfRev.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getConfRev.restype = c_uint32

    lib.ClientGooseControlBlock_getNdsComm.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getNdsComm.restype = c_bool

    lib.ClientGooseControlBlock_getMinTime.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getMinTime.restype = c_uint32

    lib.ClientGooseControlBlock_getMaxTime.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getMaxTime.restype = c_uint32

    lib.ClientGooseControlBlock_getFixedOffs.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getFixedOffs.restype = c_bool

    lib.ClientGooseControlBlock_getDstAddress.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
    ]
    lib.ClientGooseControlBlock_getDstAddress.restype = PhyComAddress

    lib.ClientGooseControlBlock_setDstAddress.argtypes = [
        ClientGooseControlBlock,  # ClientGooseControlBlock self
        PhyComAddress,  # PhyComAddress value
    ]
    lib.ClientGooseControlBlock_setDstAddress.restype = None

    ####################################################
    # GOOSE services (access to GOOSE Control Blocks (GoCB))
    ####################################################

    lib.IedConnection_getGoCBValues.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* goCBReference
        ClientGooseControlBlock,  # ClientGooseControlBlock updateGoCB
    ]
    lib.IedConnection_getGoCBValues.restype = ClientGooseControlBlock

    lib.IedConnection_getGoCBValuesAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* goCBReference
        ClientGooseControlBlock,  # ClientGooseControlBlock updateGoCB
        IedConnection_GetGoCBValuesHandler,  # IedConnection_GetGoCBValuesHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_getGoCBValuesAsync.restype = ClientGooseControlBlock

    lib.IedConnection_setGoCBValues.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        ClientGooseControlBlock,  # ClientGooseControlBlock updateGoCB
        c_uint32,  # uint32_t parametersMask,
        c_bool,  # bool singleRequest
    ]
    lib.IedConnection_setGoCBValues.restype = None

    lib.IedConnection_setGoCBValuesAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        ClientGooseControlBlock,  # ClientGooseControlBlock updateGoCB
        c_uint32,  # uint32_t parametersMask,
        c_bool,  # bool singleRequest
        IedConnection_GenericServiceHandler,  # IedConnection_GenericServiceHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_setGoCBValuesAsync.restype = None

    ####################################################
    # Data model access services
    ####################################################

    lib.IedConnection_readObject.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,  # dataAttributeReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readObject.restype = POINTER(MmsValue)

    lib.IedConnection_readObjectAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objRef
        FunctionalConstraint,  # FunctionalConstraint fc
        IedConnection_ReadObjectHandler,  # IedConnection_ReadObjectHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_readObjectAsync.restype = c_uint32

    lib.IedConnection_writeObject.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* dataAttributeReference
        FunctionalConstraint,  # FunctionalConstraint fc
        POINTER(MmsValue),  # MmsValue* value
    ]
    lib.IedConnection_writeObject.restype = None

    lib.IedConnection_writeObjectAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        POINTER(MmsValue),  # MmsValue* value
        IedConnection_GenericServiceHandler,  # IedConnection_GenericServiceHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_writeObjectAsync.restype = c_uint32

    lib.IedConnection_readBooleanValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readBooleanValue.restype = c_bool

    lib.IedConnection_readFloatValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readFloatValue.restype = c_float

    lib.IedConnection_readStringValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readStringValue.restype = c_char_p

    lib.IedConnection_readInt32Value.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readInt32Value.restype = c_int32

    lib.IedConnection_readInt64Value.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readInt64Value.restype = c_int64

    lib.IedConnection_readUnsigned32Value.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readUnsigned32Value.restype = c_uint32

    lib.IedConnection_readTimestampValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        POINTER(Timestamp),  # Timestamp* timeStamp
    ]
    lib.IedConnection_readTimestampValue.restype = POINTER(Timestamp)

    lib.IedConnection_readQualityValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.IedConnection_readQualityValue.restype = Quality

    lib.IedConnection_writeBooleanValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        c_bool,  # bool value
    ]
    lib.IedConnection_writeBooleanValue.restype = None

    lib.IedConnection_writeInt32Value.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        c_int32,  # int32_t value
    ]
    lib.IedConnection_writeInt32Value.restype = None

    lib.IedConnection_writeUnsigned32Value.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        c_uint32,  # uint32_t value
    ]
    lib.IedConnection_writeUnsigned32Value.restype = None

    lib.IedConnection_writeFloatValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        c_float,  # float value
    ]
    lib.IedConnection_writeFloatValue.restype = None

    lib.IedConnection_writeVisibleStringValue.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        c_char_p,  # char* value
    ]
    lib.IedConnection_writeVisibleStringValue.restype = None

    lib.IedConnection_writeOctetString.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* objectReference
        FunctionalConstraint,  # FunctionalConstraint fc
        c_char_p,  # uint8_t* value
        c_int,  # int valueLength
    ]
    lib.IedConnection_writeOctetString.restype = None

    ####################################################
    # Reporting services
    ####################################################

    lib.IedConnection_getRCBValues.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
        ClientReportControlBlock,
    ]
    lib.IedConnection_getRCBValues.restype = ClientReportControlBlock

    lib.IedConnection_setRCBValues.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        ClientReportControlBlock,  # ClientReportControlBlock rcb
        c_uint32,  # uint32_t parametersMask
        c_bool,  # bool singleRequest
    ]
    lib.IedConnection_setRCBValues.restype = None

    lib.IedConnection_installReportHandler.argtypes = [
        IedConnection,  # IedConnection self
        c_char_p,  # const char* rcbReference
        c_char_p,  #  const char* rptId
        ReportCallbackFunction,  # ReportCallbackFunction handler
        c_void_p,  # void* handlerParameter
    ]
    lib.IedConnection_installReportHandler.restype = None

    lib.IedConnection_uninstallReportHandler.argtypes = [
        IedConnection,  # IedConnection self
        c_char_p,  # const char* rcbReference
    ]
    lib.IedConnection_uninstallReportHandler.restype = None

    lib.IedConnection_triggerGIReport.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
    ]
    lib.IedConnection_triggerGIReport.restype = None

    ####################################################
    # Access to received reports
    ####################################################

    lib.ClientReport_getDataSetName.argtypes = [ClientReport]
    lib.ClientReport_getDataSetName.restype = c_char_p

    lib.ClientReport_getDataSetValues.argtypes = [ClientReport]
    lib.ClientReport_getDataSetValues.restype = POINTER(MmsValue)

    lib.ClientReport_getRcbReference.argtypes = [ClientReport]
    lib.ClientReport_getRcbReference.restype = c_char_p

    lib.ClientReport_getRptId.argtypes = [ClientReport]
    lib.ClientReport_getRptId.restype = c_char_p

    lib.ClientReport_getReasonForInclusion.argtypes = [ClientReport, c_int]
    lib.ClientReport_getReasonForInclusion.restype = ReasonForInclusion

    lib.ClientReport_getEntryId.argtypes = [ClientReport]
    lib.ClientReport_getEntryId.restype = POINTER(MmsValue)

    lib.ClientReport_hasTimestamp.argtypes = [ClientReport]
    lib.ClientReport_hasTimestamp.restype = c_bool

    lib.ClientReport_hasSeqNum.argtypes = [ClientReport]
    lib.ClientReport_hasSeqNum.restype = c_bool

    lib.ClientReport_getSeqNum.argtypes = [ClientReport]
    lib.ClientReport_getSeqNum.restype = c_uint16

    lib.ClientReport_hasDataSetName.argtypes = [ClientReport]
    lib.ClientReport_hasDataSetName.restype = c_bool

    lib.ClientReport_hasReasonForInclusion.argtypes = [ClientReport]
    lib.ClientReport_hasReasonForInclusion.restype = c_bool

    lib.ClientReport_hasConfRev.argtypes = [ClientReport]
    lib.ClientReport_hasConfRev.restype = c_bool

    lib.ClientReport_getConfRev.argtypes = [ClientReport]
    lib.ClientReport_getConfRev.restype = c_uint32

    lib.ClientReport_hasBufOvfl.argtypes = [ClientReport]
    lib.ClientReport_hasBufOvfl.restype = c_bool

    lib.ClientReport_getBufOvfl.argtypes = [ClientReport]
    lib.ClientReport_getBufOvfl.restype = c_bool

    lib.ClientReport_hasDataReference.argtypes = [ClientReport]
    lib.ClientReport_hasDataReference.restype = c_bool

    lib.ClientReport_getDataReference.argtypes = [
        ClientReport,  # ClientReport self
        c_int,  # int elementIndex
    ]
    lib.ClientReport_getDataReference.restype = c_char_p

    lib.ClientReport_getTimestamp.argtypes = [ClientReport]
    lib.ClientReport_getTimestamp.restype = c_uint64

    lib.ClientReport_hasSubSeqNum.argtypes = [ClientReport]
    lib.ClientReport_hasSubSeqNum.restype = c_bool

    lib.ClientReport_getSubSeqNum.argtypes = [ClientReport]
    lib.ClientReport_getSubSeqNum.restype = c_uint16

    lib.ClientReport_getMoreSeqmentsFollow.argtypes = [ClientReport]
    lib.ClientReport_getMoreSeqmentsFollow.restype = c_bool

    ####################################################
    # ClientReportControlBlock access class
    ####################################################

    lib.ClientReportControlBlock_create.argtypes = [c_char_p]
    lib.ClientReportControlBlock_create.restype = ClientReportControlBlock

    lib.ClientReportControlBlock_destroy.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_destroy.restype = None

    lib.ClientReportControlBlock_getObjectReference.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getObjectReference.restype = c_char_p

    lib.ClientReportControlBlock_isBuffered.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_isBuffered.restype = c_bool

    lib.ClientReportControlBlock_getRptId.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getRptId.restype = c_char_p

    lib.ClientReportControlBlock_setRptId.argtypes = [
        ClientReportControlBlock,
        c_char_p,
    ]
    lib.ClientReportControlBlock_setRptId.restype = None

    lib.ClientReportControlBlock_getRptEna.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getRptEna.restype = c_bool

    lib.ClientReportControlBlock_setRptEna.argtypes = [
        ClientReportControlBlock,
        c_bool,
    ]
    lib.ClientReportControlBlock_setRptEna.restype = None

    lib.ClientReportControlBlock_getResv.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getResv.restype = c_bool

    lib.ClientReportControlBlock_setResv.argtypes = [
        ClientReportControlBlock,
        c_bool,
    ]
    lib.ClientReportControlBlock_setResv.restype = None

    lib.ClientReportControlBlock_getDataSetReference.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getDataSetReference.restype = c_char_p

    lib.ClientReportControlBlock_setDataSetReference.argtypes = [
        ClientReportControlBlock,
        c_char_p,
    ]
    lib.ClientReportControlBlock_setDataSetReference.restype = None

    lib.ClientReportControlBlock_getConfRev.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getConfRev.restype = c_uint32

    lib.ClientReportControlBlock_getOptFlds.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getOptFlds.restype = c_int

    lib.ClientReportControlBlock_setOptFlds.argtypes = [
        ClientReportControlBlock,
        c_int,
    ]
    lib.ClientReportControlBlock_setOptFlds.restype = None

    lib.ClientReportControlBlock_getBufTm.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getBufTm.restype = c_uint32

    lib.ClientReportControlBlock_setBufTm.argtypes = [
        ClientReportControlBlock,
        c_uint32,
    ]
    lib.ClientReportControlBlock_setBufTm.restype = None

    lib.ClientReportControlBlock_getSqNum.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getSqNum.restype = c_uint16

    lib.ClientReportControlBlock_getTrgOps.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getTrgOps.restype = c_int

    lib.ClientReportControlBlock_setTrgOps.argtypes = [
        ClientReportControlBlock,
        c_int,
    ]
    lib.ClientReportControlBlock_setTrgOps.restype = None

    lib.ClientReportControlBlock_getIntgPd.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getIntgPd.restype = c_uint32

    lib.ClientReportControlBlock_setIntgPd.argtypes = [
        ClientReportControlBlock,
        c_uint32,
    ]
    lib.ClientReportControlBlock_setIntgPd.restype = None

    lib.ClientReportControlBlock_getGI.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getGI.restype = c_bool

    lib.ClientReportControlBlock_setGI.argtypes = [ClientReportControlBlock, c_bool]
    lib.ClientReportControlBlock_setGI.restype = None

    lib.ClientReportControlBlock_getPurgeBuf.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getPurgeBuf.restype = c_bool

    lib.ClientReportControlBlock_setPurgeBuf.argtypes = [
        ClientReportControlBlock,
        c_bool,
    ]
    lib.ClientReportControlBlock_setPurgeBuf.restype = None

    lib.ClientReportControlBlock_hasResvTms.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_hasResvTms.restype = c_bool

    lib.ClientReportControlBlock_getResvTms.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getResvTms.restype = c_uint16

    lib.ClientReportControlBlock_setResvTms.argtypes = [
        ClientReportControlBlock,
        c_uint16,
    ]
    lib.ClientReportControlBlock_setResvTms.restype = None

    lib.ClientReportControlBlock_getEntryId.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getEntryId.restype = POINTER(MmsValue)

    lib.ClientReportControlBlock_setEntryId.argtypes = [
        ClientReportControlBlock,
        c_void_p,
    ]
    lib.ClientReportControlBlock_setEntryId.restype = None

    lib.ClientReportControlBlock_getEntryTime.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getEntryTime.restype = c_uint64

    lib.ClientReportControlBlock_getOwner.argtypes = [ClientReportControlBlock]
    lib.ClientReportControlBlock_getOwner.restype = POINTER(MmsValue)

    ####################################################
    # Data set handling
    ####################################################

    lib.IedConnection_readDataSetValues.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
        ClientDataSet,
    ]
    lib.IedConnection_readDataSetValues.restype = ClientDataSet

    lib.IedConnection_createDataSet.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* dataSetReference
        LinkedList,  # LinkedList /* char* */ dataSetElements
    ]
    lib.IedConnection_createDataSet.restype = None

    lib.IedConnection_deleteDataSet.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* dataSetReference
    ]
    lib.IedConnection_deleteDataSet.restype = c_bool

    lib.IedConnection_getDataSetDirectory.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* dataSetReference
        POINTER(c_bool),  # bool* isDeletable
    ]
    lib.IedConnection_getDataSetDirectory.restype = LinkedList

    ####################################################
    # Data set object (local representation of a data set)
    ####################################################

    lib.ClientDataSet_destroy.argtypes = [
        ClientDataSet,  # ClientDataSet self
    ]
    lib.ClientDataSet_destroy.restype = None

    lib.ClientDataSet_getValues.argtypes = [
        ClientDataSet,  # ClientDataSet self
    ]
    lib.ClientDataSet_getValues.restype = POINTER(MmsValue)

    lib.ClientDataSet_getReference.argtypes = [
        ClientDataSet,  # ClientDataSet self
    ]
    lib.ClientDataSet_getReference.restype = c_char_p

    lib.ClientDataSet_getDataSetSize.argtypes = [
        ClientDataSet,  # ClientDataSet self
    ]
    lib.ClientDataSet_getDataSetSize.restype = c_int

    ####################################################
    # Control service functions
    ####################################################

    lib.ControlObjectClient_create.argtypes = [
        c_char_p,  # const char* objectReference
        IedConnection,  # IedConnection connection
    ]
    lib.ControlObjectClient_create.restype = ControlObjectClient

    lib.ControlObjectClient_createEx.argtypes = [
        c_char_p,  # const char* objectReference
        IedConnection,  # IedConnection connection
        ControlModel,  # ControlModel ctlModel
        MmsVariableSpecification,  # MmsVariableSpecification* controlObjectSpec
    ]
    lib.ControlObjectClient_createEx.restype = ControlObjectClient

    lib.ControlObjectClient_destroy.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_destroy.restype = None

    lib.ControlObjectClient_getObjectReference.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_getObjectReference.restype = c_char_p

    lib.ControlObjectClient_getControlModel.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_getControlModel.restype = ControlModel

    lib.ControlObjectClient_setControlModel.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        ControlModel,  # ControlModel ctlModel
    ]
    lib.ControlObjectClient_setControlModel.restype = None

    lib.ControlObjectClient_changeServerControlModel.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        ControlModel,  # ControlModel ctlModel
    ]
    lib.ControlObjectClient_changeServerControlModel.restype = None

    lib.ControlObjectClient_getCtlValType.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_getCtlValType.restype = MmsType

    lib.ControlObjectClient_getLastError.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_getLastError.restype = IedClientError

    lib.ControlObjectClient_operate.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        POINTER(MmsValue),  # MmsValue* ctlVal,
        c_uint64,  # uint64_t operTime
    ]
    lib.ControlObjectClient_operate.restype = c_bool

    lib.ControlObjectClient_select.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_select.restype = c_bool

    lib.ControlObjectClient_selectWithValue.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        POINTER(MmsValue),  # MmsValue* ctlVal,
    ]
    lib.ControlObjectClient_selectWithValue.restype = c_bool

    lib.ControlObjectClient_cancel.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_cancel.restype = c_bool

    lib.ControlObjectClient_operateAsync.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        POINTER(IedClientError),  # IedClientError* err,
        POINTER(MmsValue),  # MmsValue* ctlVal,
        c_uint64,  # uint64_t operTime
        ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler,
        c_void_p,  # void* parameter
    ]
    lib.ControlObjectClient_operateAsync.restype = c_uint32

    lib.ControlObjectClient_selectAsync.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        POINTER(IedClientError),  # IedClientError* err,
        ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler,
        c_void_p,  # void* parameter
    ]
    lib.ControlObjectClient_selectAsync.restype = c_uint32

    lib.ControlObjectClient_selectWithValueAsync.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        POINTER(IedClientError),  # IedClientError* err
        POINTER(MmsValue),  # MmsValue* ctlVal
        ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler
        c_void_p,  #  void* parameter
    ]
    lib.ControlObjectClient_selectWithValueAsync.restype = c_uint32

    lib.ControlObjectClient_cancelAsync.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        POINTER(IedClientError),  # IedClientError* err
        ControlObjectClient_ControlActionHandler,  # ControlObjectClient_ControlActionHandler handler
        c_void_p,  #  void* parameter
    ]
    lib.ControlObjectClient_cancelAsync.restype = c_uint32

    lib.ControlObjectClient_getLastApplError.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
    ]
    lib.ControlObjectClient_getLastApplError.restype = LastApplError

    lib.ControlObjectClient_setTestMode.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        c_bool,  # bool value
    ]
    lib.ControlObjectClient_setTestMode.restype = None

    lib.ControlObjectClient_setOrigin.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        c_char_p,  # const char* orIdent
        c_int,  # int orCat
    ]
    lib.ControlObjectClient_setOrigin.restype = None

    lib.ControlObjectClient_useConstantT.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        c_bool,  # bool useConstantT
    ]
    lib.ControlObjectClient_useConstantT.restype = None

    lib.ControlObjectClient_setInterlockCheck.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        c_bool,  # bool value
    ]
    lib.ControlObjectClient_setInterlockCheck.restype = None

    lib.ControlObjectClient_setSynchroCheck.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        c_bool,  # bool value
    ]
    lib.ControlObjectClient_setSynchroCheck.restype = None

    lib.ControlObjectClient_setCommandTerminationHandler.argtypes = [
        ControlObjectClient,  # ControlObjectClient self
        CommandTerminationHandler,  # CommandTerminationHandler handler
        c_void_p,  # void* handlerParameter
    ]
    lib.ControlObjectClient_setCommandTerminationHandler.restype = None

    ####################################################
    # Model discovery services
    ####################################################

    lib.IedConnection_getServerDirectory.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_bool,
    ]
    lib.IedConnection_getServerDirectory.restype = LinkedList

    lib.IedConnection_getLogicalDeviceDirectory.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
    ]
    lib.IedConnection_getLogicalDeviceDirectory.restype = LinkedList

    lib.IedConnection_getLogicalNodeVariables.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
    ]
    lib.IedConnection_getLogicalNodeVariables.restype = LinkedList

    lib.IedConnection_getLogicalNodeDirectory.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
        ACSIClass,
    ]
    lib.IedConnection_getLogicalNodeDirectory.restype = LinkedList

    lib.IedConnection_getDataDirectory.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
    ]
    lib.IedConnection_getDataDirectory.restype = LinkedList

    lib.IedConnection_getDataDirectoryFC.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
    ]
    lib.IedConnection_getDataDirectoryFC.restype = LinkedList

    lib.IedConnection_getDataDirectoryByFC.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
        FunctionalConstraint,
    ]
    lib.IedConnection_getDataDirectoryByFC.restype = LinkedList

    lib.IedConnection_getLogicalDeviceVariables.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
    ]
    lib.IedConnection_getLogicalDeviceVariables.restype = LinkedList

    lib.IedConnection_getLogicalDeviceDataSets.argtypes = [
        IedConnection,
        POINTER(IedClientError),
        c_char_p,
    ]
    lib.IedConnection_getLogicalDeviceDataSets.restype = LinkedList

    ####################################################
    # Asynchronous model discovery functions
    ####################################################

    lib.IedConnection_getServerDirectoryAsync.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* continueAfter
        LinkedList,  # LinkedList result
        IedConnection_GetNameListHandler,  # IedConnection_GetNameListHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_getServerDirectoryAsync.restype = c_uint32

    lib.IedConnection_getLogicalDeviceVariablesAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* ldName
        c_char_p,  # const char* continueAfter
        LinkedList,  # LinkedList result
        IedConnection_GetNameListHandler,  # IedConnection_GetNameListHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_getLogicalDeviceVariablesAsync.restype = c_uint32

    lib.IedConnection_getLogicalDeviceDataSetsAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* ldName
        c_char_p,  #  const char* continueAfter
        LinkedList,  # LinkedList result
        IedConnection_GetNameListHandler,  # IedConnection_GetNameListHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_getLogicalDeviceDataSetsAsync.restype = c_uint32

    lib.IedConnection_getVariableSpecificationAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* dataAttributeReference
        FunctionalConstraint,  #  FunctionalConstraint fc
        IedConnection_GetVariableSpecificationHandler,  # IedConnection_GetVariableSpecificationHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_getVariableSpecificationAsync.restype = c_uint32

    lib.IedConnection_queryLogByTime.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* logReference
        c_uint64,  #  uint64_t startTime
        c_uint64,  # uint64_t endTime
        POINTER(c_bool),  # bool* moreFollows
    ]
    lib.IedConnection_queryLogByTime.restype = LinkedList

    lib.IedConnection_queryLogAfter.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* logReference
        POINTER(MmsValue),  #  MmsValue* entryID
        c_uint64,  # uint64_t timeStamp
        POINTER(c_bool),  # bool* moreFollows
    ]
    lib.IedConnection_queryLogAfter.restype = LinkedList

    lib.IedConnection_queryLogByTimeAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* logReference
        c_uint64,  #  uint64_t startTime
        c_uint64,  # uint64_t endTime
        IedConnection_QueryLogHandler,  # IedConnection_QueryLogHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_queryLogByTimeAsync.restype = c_uint32

    lib.IedConnection_queryLogAfterAsync.argtypes = [
        IedConnection,  # IedConnection self
        POINTER(IedClientError),  # IedClientError* error
        c_char_p,  # const char* logReference
        POINTER(MmsValue),  #  MmsValue* entryID
        c_uint64,  # uint64_t timeStamp
        IedConnection_QueryLogHandler,  # IedConnection_QueryLogHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_queryLogAfterAsync.restype = c_uint32

    ####################################################
    # File directory
    ####################################################

    lib.FileDirectoryEntry_create.argtypes = [
        c_char_p,  # const char* fileName
        c_uint32,  # uint32_t fileSize
        c_uint64,  # uint64_t lastModified
    ]
    lib.FileDirectoryEntry_create.restype = FileDirectoryEntry

    lib.FileDirectoryEntry_destroy.argtypes = [
        FileDirectoryEntry,  # FileDirectoryEntry self
    ]
    lib.FileDirectoryEntry_destroy.restype = None

    lib.FileDirectoryEntry_getFileName.argtypes = [
        FileDirectoryEntry,  # FileDirectoryEntry self
    ]
    lib.FileDirectoryEntry_getFileName.restype = c_char_p

    lib.FileDirectoryEntry_getFileSize.argtypes = [
        FileDirectoryEntry,  # FileDirectoryEntry self
    ]
    lib.FileDirectoryEntry_getFileSize.restype = c_uint32

    lib.FileDirectoryEntry_getLastModified.argtypes = [
        FileDirectoryEntry,  # FileDirectoryEntry self
    ]
    lib.FileDirectoryEntry_getLastModified.restype = c_uint64

    lib.IedConnection_getFileDirectory.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* directoryName
    ]
    lib.IedConnection_getFileDirectory.restype = LinkedList

    lib.IedConnection_getFileDirectoryEx.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* directoryName
        c_char_p,  # const char* continueAfter
        POINTER(c_bool),  # bool* moreFollows
    ]
    lib.IedConnection_getFileDirectoryEx.restype = LinkedList

    lib.IedConnection_getFileDirectoryAsyncEx.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* directoryName
        c_char_p,  # const char* continueAfter
        IedConnection_FileDirectoryEntryHandler,  # IedConnection_FileDirectoryEntryHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_getFileDirectoryAsyncEx.restype = c_uint32

    lib.IedConnection_getFile.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* fileName,
        IedClientGetFileHandler,  # IedClientGetFileHandler handler,
        c_void_p,  # void* handlerParameter
    ]
    lib.IedConnection_getFile.restype = c_uint32

    lib.IedConnection_getFileAsync.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* fileName,
        IedConnection_GetFileAsyncHandler,  # IedConnection_GetFileAsyncHandler handler,
        c_void_p,  # void* hanparameterdlerParameter
    ]
    lib.IedConnection_getFileAsync.restype = c_uint32

    lib.IedConnection_setFilestoreBasepath.argtypes = [
        IedConnection,  # IedConnection self,
        c_char_p,  # const char* basepath
    ]
    lib.IedConnection_setFilestoreBasepath.restype = None

    lib.IedConnection_setFile.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* sourceFilename,
        c_char_p,  # const char* destinationFilename
    ]
    lib.IedConnection_setFile.restype = None

    lib.IedConnection_setFileAsync.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* sourceFilename,
        c_char_p,  # const char* destinationFilename
        IedConnection_GenericServiceHandler,  # IedConnection_GenericServiceHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_setFileAsync.restype = c_uint32

    lib.IedConnection_deleteFile.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* fileName,
    ]
    lib.IedConnection_deleteFile.restype = None

    lib.IedConnection_deleteFileAsync.argtypes = [
        IedConnection,  # IedConnection self,
        POINTER(IedClientError),  # IedClientError* error,
        c_char_p,  # const char* fileName,
        IedConnection_GenericServiceHandler,  # IedConnection_GenericServiceHandler handler
        c_void_p,  # void* parameter
    ]
    lib.IedConnection_deleteFileAsync.restype = c_uint32
