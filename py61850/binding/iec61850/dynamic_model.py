"""Module for C binding with iec61850/inc/iec61850_dynamic_model.h"""

from ctypes import (
    CDLL,
    POINTER,
    c_bool,
    c_char_p,
    c_int,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
)

from ..mms import MmsValue
from .iec61850_common import FunctionalConstraint, PhyComAddress
from .model import (
    DataAttribute,
    DataAttributeType,
    DataObject,
    DataSet,
    DataSetEntry,
    GSEControlBlock,
    IedModel,
    Log,
    LogControlBlock,
    LogicalDevice,
    LogicalNode,
    ModelNode,
    ReportControlBlock,
    SettingGroupControlBlock,
    SVControlBlock,
)


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    lib.IedModel_create.argtypes = [
        c_char_p,  # const char* name
    ]
    lib.IedModel_create.restype = POINTER(IedModel)

    lib.IedModel_setIedNameForDynamicModel.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_char_p,  # const char* name
    ]
    lib.IedModel_setIedNameForDynamicModel.restype = None

    lib.IedModel_destroy.argtypes = [
        POINTER(IedModel),  # IedModel* self
    ]
    lib.IedModel_destroy.restype = None

    lib.LogicalDevice_create.argtypes = [
        c_char_p,  # const char* inst
        POINTER(IedModel),  # IedModel* parent
    ]
    lib.LogicalDevice_create.restype = POINTER(LogicalDevice)

    lib.LogicalDevice_createEx.argtypes = [
        c_char_p,  # const char* inst
        POINTER(IedModel),  # IedModel* parent
        c_char_p,  # const char* ldName
    ]
    lib.LogicalDevice_createEx.restype = POINTER(LogicalDevice)

    lib.LogicalNode_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(LogicalDevice),  # LogicalDevice* parent
    ]
    lib.LogicalNode_create.restype = POINTER(LogicalNode)

    lib.DataObject_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* name
        c_int,  # int arrayElements
    ]
    lib.DataObject_create.restype = POINTER(DataObject)

    lib.DataAttribute_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* parent
        DataAttributeType,  # DataAttributeType type
        FunctionalConstraint,  # FunctionalConstraint fc
        c_uint8,  # uint8_t triggerOptions
        c_int,  #  int arrayElements
        c_uint32,  #  uint32_t sAddr
    ]
    lib.DataAttribute_create.restype = POINTER(DataAttribute)

    lib.DataAttribute_getType.argtypes = [
        POINTER(DataAttribute),  # DataAttribute* self
    ]
    lib.DataAttribute_getType.restype = DataAttributeType

    lib.DataAttribute_getFC.argtypes = [
        POINTER(DataAttribute),  # DataAttribute* self
    ]
    lib.DataAttribute_getFC.restype = FunctionalConstraint

    lib.DataAttribute_getTrgOps.argtypes = [
        POINTER(DataAttribute),  # DataAttribute* self
    ]
    lib.DataAttribute_getTrgOps.restype = c_uint8

    lib.DataAttribute_setValue.argtypes = [
        POINTER(DataAttribute),  # DataAttribute* self
        POINTER(MmsValue),  # MmsValue* value
    ]
    lib.DataAttribute_setValue.restype = None

    lib.ReportControlBlock_create.argtypes = [
        c_char_p,  # const char* name,
        POINTER(LogicalNode),  # LogicalNode* parent,
        c_char_p,  # const char* rptId,
        c_bool,  #  bool isBuffered,
        c_char_p,  # const char* dataSetName,
        c_uint32,  #  uint32_t confRef,
        c_uint8,  #  uint8_t trgOps,
        c_uint8,  # uint8_t options,
        c_uint32,  #  uint32_t bufTm,
        c_uint32,  # uint32_t intgPd
    ]
    lib.DataAttribute_setValue.restype = POINTER(ReportControlBlock)

    lib.ReportControlBlock_setPreconfiguredClient.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
        c_uint8,  # uint8_t clientType
        POINTER(c_uint8),  # const uint8_t* clientAddress
    ]
    lib.ReportControlBlock_setPreconfiguredClient.restype = None

    lib.ReportControlBlock_getName.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getName.restype = c_char_p

    lib.ReportControlBlock_isBuffered.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_isBuffered.restype = c_bool

    lib.ReportControlBlock_getParent.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getParent.restype = POINTER(LogicalNode)

    lib.ReportControlBlock_getRptID.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getRptID.restype = c_char_p

    lib.ReportControlBlock_getRptEna.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getRptEna.restype = c_bool

    lib.ReportControlBlock_getDataSet.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getDataSet.restype = c_char_p

    lib.ReportControlBlock_getConfRev.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getConfRev.restype = c_uint32

    lib.ReportControlBlock_getOptFlds.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getOptFlds.restype = c_uint32

    lib.ReportControlBlock_getBufTm.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getBufTm.restype = c_uint32

    lib.ReportControlBlock_getSqNum.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getSqNum.restype = c_uint16

    lib.ReportControlBlock_getTrgOps.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getTrgOps.restype = c_uint32

    lib.ReportControlBlock_getIntgPd.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getIntgPd.restype = c_uint32

    lib.ReportControlBlock_getGI.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getGI.restype = c_bool

    lib.ReportControlBlock_getPurgeBuf.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getPurgeBuf.restype = c_bool

    lib.ReportControlBlock_getEntryId.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getEntryId.restype = POINTER(MmsValue)

    lib.ReportControlBlock_getTimeofEntry.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getTimeofEntry.restype = c_uint64

    lib.ReportControlBlock_getResvTms.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getResvTms.restype = c_uint16

    lib.ReportControlBlock_getResv.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getResv.restype = c_bool

    lib.ReportControlBlock_getOwner.argtypes = [
        POINTER(ReportControlBlock),  # ReportControlBlock* self
    ]
    lib.ReportControlBlock_getOwner.restype = POINTER(MmsValue)

    lib.LogControlBlock_create.argtypes = [
        c_char_p,  # const char* name,
        POINTER(LogicalNode),  # LogicalNode* parent,
        c_char_p,  #  const char* dataSetName,
        c_char_p,  # const char* logRef,
        c_uint8,  # uint8_t trgOps,
        c_uint32,  # uint32_t intgPd,
        c_bool,  #  bool logEna,
        c_bool,  # bool reasonCode
    ]
    lib.LogControlBlock_create.restype = POINTER(LogControlBlock)

    lib.LogControlBlock_getName.argtypes = [
        POINTER(LogControlBlock),  # LogControlBlock* self
    ]
    lib.LogControlBlock_getName.restype = c_char_p

    lib.LogControlBlock_getParent.argtypes = [
        POINTER(LogControlBlock),  # LogControlBlock* self
    ]
    lib.LogControlBlock_getParent.restype = POINTER(LogicalNode)

    lib.Log_create.argtypes = [
        c_char_p,  # const char* name,
        POINTER(LogicalNode),  # LogicalNode* parent,
    ]
    lib.Log_create.restype = POINTER(Log)

    lib.SettingGroupControlBlock_create.argtypes = [
        POINTER(LogicalNode),  # LogicalNode* parent,
        c_uint8,  # uint8_t actSG,
        c_uint8,  # uint8_t numOfSGs
    ]
    lib.SettingGroupControlBlock_create.restype = POINTER(SettingGroupControlBlock)

    lib.GSEControlBlock_create.argtypes = [
        c_char_p,  # const char* name,
        POINTER(LogicalNode),  # LogicalNode* parent,
        c_char_p,  #  const char* appId,
        c_char_p,  # const char* dataSet,
        c_uint32,  #  uint32_t confRev,
        c_bool,  # bool fixedOffs,
        c_int,  # int minTime,
        c_int,  # int maxTime
    ]
    lib.GSEControlBlock_create.restype = POINTER(GSEControlBlock)

    lib.SVControlBlock_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(LogicalNode),  # LogicalNode* parent
        c_char_p,  # c const char* svID
        c_char_p,  # const char* dataSet
        c_uint32,  # uint32_t confRev
        c_uint8,  # uint8_t smpMod
        c_uint16,  # uint16_t smpRate
        c_uint8,  # uint8_t optFlds
        c_bool,  #  bool isUnicast
    ]
    lib.SVControlBlock_create.restype = POINTER(SVControlBlock)

    lib.SVControlBlock_getName.argtypes = [
        POINTER(SVControlBlock),  # SVControlBlock* self
    ]
    lib.SVControlBlock_getName.restype = c_char_p

    lib.SVControlBlock_addPhyComAddress.argtypes = [
        POINTER(SVControlBlock),  # SVControlBlock* self
        POINTER(PhyComAddress),  # PhyComAddress* phyComAddress
    ]
    lib.SVControlBlock_addPhyComAddress.restype = None

    lib.GSEControlBlock_addPhyComAddress.argtypes = [
        POINTER(GSEControlBlock),  # GSEControlBlock* self
        POINTER(PhyComAddress),  # PhyComAddress* phyComAddress
    ]
    lib.GSEControlBlock_addPhyComAddress.restype = None

    lib.PhyComAddress_create.argtypes = [
        c_uint8,  # uint8_t vlanPriority
        c_uint16,  # uint16_t vlanId
        c_uint16,  # uint16_t appId
        POINTER(c_uint8),  # uint8_t dstAddress[]
    ]
    lib.PhyComAddress_create.restype = POINTER(PhyComAddress)

    lib.DataSet_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(LogicalNode),  # LogicalNode* parent
    ]
    lib.DataSet_create.restype = POINTER(DataSet)

    lib.DataSet_getName.argtypes = [
        POINTER(DataSet),  # DataSet* self
    ]
    lib.DataSet_getName.restype = c_char_p

    lib.DataSet_getSize.argtypes = [
        POINTER(DataSet),  # DataSet* self
    ]
    lib.DataSet_getSize.restype = c_int

    lib.DataSet_getFirstEntry.argtypes = [
        POINTER(DataSet),  # DataSet* self
    ]
    lib.DataSet_getFirstEntry.restype = POINTER(DataSetEntry)

    lib.DataSetEntry_getNext.argtypes = [
        POINTER(DataSetEntry),  # DataSetEntry* self
    ]
    lib.DataSetEntry_getNext.restype = POINTER(DataSetEntry)

    lib.DataSetEntry_create.argtypes = [
        POINTER(DataSet),  # DataSet* dataSet
        c_char_p,  # const char* variable
        c_int,  # int index
        c_char_p,  # const char* component
    ]
    lib.DataSetEntry_create.restype = POINTER(DataSetEntry)
