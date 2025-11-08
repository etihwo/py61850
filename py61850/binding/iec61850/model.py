"""Module for C binding with iec61850/inc/iec61850_model.h"""

from ctypes import (
    CDLL,
    POINTER,
    Structure,
    c_bool,
    c_char_p,
    c_int,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_void_p,
)

from ..common.linked_list import LinkedList
from ..mms import MmsValue
from .iec61850_common import FunctionalConstraint

ModelNodeType = c_int
DataAttributeType = c_int


class ModelNode(Structure):
    pass


ModelNode._fields_ = [
    ("modelType", ModelNodeType),
    ("name", c_char_p),
    ("parent", POINTER(ModelNode)),
    ("sibling", POINTER(ModelNode)),
    ("firstChild", POINTER(ModelNode)),
]


class DataAttribute(Structure):
    _fields_ = [
        ("modelType", ModelNodeType),
        ("name", c_char_p),  # Corresponds to inst attribute
        ("parent", POINTER(ModelNode)),
        ("sibling", POINTER(ModelNode)),
        ("firstChild", POINTER(ModelNode)),
        ("elementCount", c_int),  # value > 0 if this is an array
        ("arrayIndex", c_int),  # value > -1 when this is an array element
        ("fc", FunctionalConstraint),
        ("type", DataAttributeType),
        (
            "triggerOptions",
            c_uint8,
        ),  # TRG_OPT_DATA_CHANGED | TRG_OPT_QUALITY_CHANGED | TRG_OPT_DATA_UPDATE
        ("mmsValue", POINTER(MmsValue)),
    ]


class DataObject(Structure):
    _fields_ = [
        ("modelType", ModelNodeType),
        ("name", c_char_p),  # Corresponds to inst attribute
        ("parent", POINTER(ModelNode)),
        ("sibling", POINTER(ModelNode)),
        ("firstChild", POINTER(ModelNode)),
        ("elementCount", c_int),  # value > 0 if this is an array
        ("arrayIndex", c_int),  # value > -1 when this is an array element
    ]


class LogicalNode(Structure):
    _fields_ = [
        ("modelType", ModelNodeType),
        ("name", c_char_p),  # Corresponds to inst attribute
        ("parent", POINTER(ModelNode)),
        ("sibling", POINTER(ModelNode)),
        ("firstChild", POINTER(ModelNode)),
    ]


class LogicalDevice(Structure):
    _fields_ = [
        ("modelType", ModelNodeType),
        ("name", c_char_p),  # Corresponds to inst attribute
        ("parent", POINTER(ModelNode)),
        ("sibling", POINTER(ModelNode)),
        ("firstChild", POINTER(ModelNode)),
        ("ldName", c_char_p),
    ]


class DataSetEntry(Structure): ...


class DataSet(Structure): ...


class ReportControlBlock(Structure): ...


class SettingGroupControlBlock(Structure): ...


SettingGroupControlBlock._fields_ = [
    ("parent", POINTER(LogicalNode)),
    ("actSG", c_uint8),
    ("numOfSGs", c_uint8),
    ("editSG", c_uint8),
    ("cnfEdit", c_bool),
    ("timestamp", c_uint64),
    ("resvTms", c_uint16),
    ("sibling", POINTER(SettingGroupControlBlock)),
]


class GSEControlBlock(Structure): ...


class SVControlBlock(Structure): ...


class LogControlBlock(Structure): ...


class Log(Structure): ...


class IedModel(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("firstChild", POINTER(LogicalDevice)),
        ("dataSets", POINTER(DataSet)),
        ("rcbs", POINTER(ReportControlBlock)),
        ("gseCBs", POINTER(GSEControlBlock)),
        ("svCBs", POINTER(SVControlBlock)),
        ("sgcbs", POINTER(SettingGroupControlBlock)),
        ("lcbs", POINTER(LogControlBlock)),
        ("logs", POINTER(Log)),
        ("initializer", c_void_p),
    ]


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    lib.ModelNode_getChildCount.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
    ]
    lib.ModelNode_getChildCount.restype = c_int

    lib.ModelNode_getChild.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
        c_char_p,  # const char* name
    ]
    lib.ModelNode_getChild.restype = POINTER(ModelNode)

    lib.ModelNode_getChildWithIdx.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
        c_int,  # int idx
    ]
    lib.ModelNode_getChildWithIdx.restype = POINTER(ModelNode)

    lib.ModelNode_getChildWithFc.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
        c_char_p,  # const char* name,
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.ModelNode_getChildWithFc.restype = POINTER(ModelNode)

    lib.ModelNode_getObjectReference.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
        c_char_p,  #  char* objectReference
    ]
    lib.ModelNode_getObjectReference.restype = c_char_p

    lib.ModelNode_getObjectReferenceEx.argtypes = [
        POINTER(ModelNode),  # ModelNode* node
        c_char_p,  #  char* objectReference
        c_bool,  #  bool withoutIedName
    ]
    lib.ModelNode_getObjectReferenceEx.restype = c_char_p

    lib.ModelNode_getType.argtypes = [
        POINTER(ModelNode),  # ModelNode* node
    ]
    lib.ModelNode_getType.restype = ModelNodeType

    lib.ModelNode_getName.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
    ]
    lib.ModelNode_getName.restype = c_char_p

    lib.ModelNode_getParent.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
    ]
    lib.ModelNode_getParent.restype = POINTER(ModelNode)

    lib.ModelNode_getChildren.argtypes = [
        POINTER(ModelNode),  # ModelNode* self
    ]
    lib.ModelNode_getChildren.restype = LinkedList

    lib.IedModel_setIedName.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_char_p,  # const char* iedName
    ]
    lib.IedModel_setIedName.restype = None

    lib.IedModel_getModelNodeByObjectReference.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_char_p,  # const char* objectReference
    ]
    lib.IedModel_getModelNodeByObjectReference.restype = POINTER(ModelNode)

    lib.IedModel_getSVControlBlock.argtypes = [
        POINTER(IedModel),  # IedModel* self
        POINTER(LogicalNode),  # LogicalNode* parentLN,
        c_char_p,  # const char* svcbName
    ]
    lib.IedModel_getSVControlBlock.restype = POINTER(SVControlBlock)

    lib.IedModel_getModelNodeByShortObjectReference.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_char_p,  # const char* objectReference
    ]
    lib.IedModel_getModelNodeByShortObjectReference.restype = POINTER(ModelNode)

    lib.IedModel_getModelNodeByShortAddress.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_uint32,  # uint32_t shortAddress
    ]
    lib.IedModel_getModelNodeByShortAddress.restype = POINTER(ModelNode)

    lib.IedModel_getDeviceByInst.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_char_p,  # const char* ldInst
    ]
    lib.IedModel_getDeviceByInst.restype = POINTER(LogicalDevice)

    lib.IedModel_getDeviceByIndex.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_int,  # int index
    ]
    lib.IedModel_getDeviceByIndex.restype = POINTER(LogicalDevice)

    lib.LogicalDevice_getLogicalNode.argtypes = [
        POINTER(LogicalDevice),  # LogicalDevice* self
        c_char_p,  # const char* lnName
    ]
    lib.LogicalDevice_getLogicalNode.restype = POINTER(LogicalNode)

    lib.LogicalDevice_getSettingGroupControlBlock.argtypes = [
        POINTER(LogicalDevice),  # LogicalDevice* self
    ]
    lib.LogicalDevice_getSettingGroupControlBlock.restype = POINTER(SettingGroupControlBlock)

    lib.IedModel_setAttributeValuesToNull.argtypes = [
        POINTER(IedModel),  # IedModel* self
    ]
    lib.IedModel_setAttributeValuesToNull.restype = None

    lib.IedModel_getDevice.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_char_p,  # const char* ldName
    ]
    lib.IedModel_getDevice.restype = POINTER(LogicalDevice)

    lib.IedModel_lookupDataSet.argtypes = [
        POINTER(IedModel),  # IedModel* self
        c_char_p,  # const char* dataSetReference
    ]
    lib.IedModel_lookupDataSet.restype = POINTER(DataSet)

    lib.IedModel_lookupDataSet.argtypes = [
        POINTER(IedModel),  # IedModel* self
        POINTER(MmsValue),  # MmsValue* value
    ]
    lib.IedModel_lookupDataSet.restype = POINTER(DataAttribute)

    lib.IedModel_getLogicalDeviceCount.argtypes = [
        POINTER(IedModel),  # IedModel* self
    ]
    lib.IedModel_getLogicalDeviceCount.restype = c_int

    lib.LogicalDevice_getLogicalNodeCount.argtypes = [
        POINTER(LogicalDevice),  # LogicalDevice* self
    ]
    lib.LogicalDevice_getLogicalNodeCount.restype = c_int

    lib.LogicalDevice_getLogicalNodeCount.argtypes = [
        POINTER(LogicalDevice),  # LogicalDevice* self
        c_char_p,  # const char* mmsVariableName
    ]
    lib.LogicalDevice_getLogicalNodeCount.restype = POINTER(ModelNode)

    lib.LogicalNode_hasFCData.argtypes = [
        POINTER(LogicalNode),  # LogicalNode* self
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.LogicalNode_hasFCData.restype = c_bool

    lib.ModelNode_getChildWithIdx.argtypes = [
        POINTER(DataObject),  # DataObject* self
        FunctionalConstraint,  # FunctionalConstraint fc
    ]
    lib.ModelNode_getChildWithIdx.restype = c_bool
