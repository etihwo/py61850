"""Module for C binding with iec61850/inc/iec61850_cdc.h"""

from ctypes import CDLL, POINTER, c_bool, c_char_p, c_uint8, c_uint16, c_uint32

from .iec61850_common import FunctionalConstraint
from .model import DataAttribute, DataObject, ModelNode


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    ####################################################
    # Constructed Attribute Classes (CAC)
    ####################################################

    lib.CAC_AnalogueValue_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* parent
        FunctionalConstraint,  #  FunctionalConstraint fc
        c_uint8,  #  uint8_t triggerOptions
        c_bool,  # bool isIntegerNotFloat
    ]
    lib.CAC_AnalogueValue_create.restype = POINTER(DataAttribute)

    lib.CAC_ValWithTrans_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* parent
        FunctionalConstraint,  #  FunctionalConstraint fc
        c_uint8,  #  uint8_t triggerOptions
        c_bool,  # bool hasTransientIndicator
    ]
    lib.CAC_ValWithTrans_create.restype = POINTER(DataAttribute)

    lib.CAC_Vector_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  #  uint32_t options
        FunctionalConstraint,  #  FunctionalConstraint fc
        c_uint8,  #  uint8_t triggerOptions
    ]
    lib.CAC_Vector_create.restype = POINTER(DataAttribute)

    lib.CAC_Point_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* parent
        FunctionalConstraint,  #  FunctionalConstraint fc
        c_uint8,  #  uint8_t triggerOptions
        c_bool,  # bool hasZVal
    ]
    lib.CAC_Point_create.restype = POINTER(DataAttribute)

    lib.CAC_ScaledValueConfig_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* parent
    ]
    lib.CAC_ScaledValueConfig_create.restype = POINTER(DataAttribute)

    lib.CAC_Unit_create.argtypes = [
        c_char_p,  # const char* name
        POINTER(ModelNode),  # ModelNode* parent
        c_bool,  # bool hasMagnitude
    ]
    lib.CAC_Unit_create.restype = POINTER(DataAttribute)

    ####################################################
    # Common Data Classes (CDC)
    ####################################################

    lib.CDC_SPS_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_SPS_create.restype = POINTER(DataObject)

    lib.CDC_DPS_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_DPS_create.restype = POINTER(DataObject)

    lib.CDC_INS_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_INS_create.restype = POINTER(DataObject)

    lib.CDC_ENS_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_ENS_create.restype = POINTER(DataObject)

    lib.CDC_BCR_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_BCR_create.restype = POINTER(DataObject)

    lib.CDC_VSS_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_VSS_create.restype = POINTER(DataObject)

    lib.CDC_SEC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_SEC_create.restype = POINTER(DataObject)

    lib.CDC_MV_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_bool,  # bool isIntegerNotFloat
    ]
    lib.CDC_MV_create.restype = POINTER(DataObject)

    lib.CDC_CMV_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_CMV_create.restype = POINTER(DataObject)

    lib.CDC_SAV_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_bool,  # bool isIntegerNotFloat
    ]
    lib.CDC_SAV_create.restype = POINTER(DataObject)

    lib.CDC_LPL_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_LPL_create.restype = POINTER(DataObject)

    lib.CDC_HST_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint16,  # uint16_t maxPts
    ]
    lib.CDC_HST_create.restype = POINTER(DataObject)

    lib.CDC_ACD_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_ACD_create.restype = POINTER(DataObject)

    lib.CDC_ACT_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_ACT_create.restype = POINTER(DataObject)

    lib.CDC_SPG_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_SPG_create.restype = POINTER(DataObject)

    lib.CDC_VSG_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_VSG_create.restype = POINTER(DataObject)

    lib.CDC_ENG_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_ENG_create.restype = POINTER(DataObject)

    lib.CDC_ING_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_ING_create.restype = POINTER(DataObject)

    lib.CDC_ASG_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_bool,  # bool isIntegerNotFloat
    ]
    lib.CDC_ASG_create.restype = POINTER(DataObject)

    lib.CDC_WYE_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_WYE_create.restype = POINTER(DataObject)

    lib.CDC_DEL_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
    ]
    lib.CDC_DEL_create.restype = POINTER(DataObject)

    ####################################################
    # Controls
    ####################################################

    lib.CDC_SPC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
    ]
    lib.CDC_SPC_create.restype = POINTER(DataObject)

    lib.CDC_DPC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
    ]
    lib.CDC_DPC_create.restype = POINTER(DataObject)

    lib.CDC_INC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
    ]
    lib.CDC_INC_create.restype = POINTER(DataObject)

    lib.CDC_ENC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
    ]
    lib.CDC_ENC_create.restype = POINTER(DataObject)

    lib.CDC_BSC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_bool,  # bool hasTransientIndicator
    ]
    lib.CDC_BSC_create.restype = POINTER(DataObject)

    lib.CDC_ISC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_bool,  # bool hasTransientIndicator
    ]
    lib.CDC_ISC_create.restype = POINTER(DataObject)

    lib.CDC_APC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_bool,  # bool isIntegerNotFloat
    ]
    lib.CDC_APC_create.restype = POINTER(DataObject)

    lib.CDC_BAC_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_bool,  # bool isIntegerNotFloat
    ]
    lib.CDC_BAC_create.restype = POINTER(DataObject)

    lib.CDC_SPV_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_uint32,  # uint32_t wpOptions
        c_bool,  # bool hasChaManRs
    ]
    lib.CDC_SPV_create.restype = POINTER(DataObject)

    lib.CDC_STV_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_uint32,  # uint32_t wpOptions
        c_bool,  # bool hasOldStatus
    ]
    lib.CDC_STV_create.restype = POINTER(DataObject)

    lib.CDC_CMD_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_uint32,  # uint32_t wpOptions
        c_bool,  # bool hasOldStatus
        c_bool,  # bool hasCmTm,
        c_bool,  # bool hasCmCt
    ]
    lib.CDC_CMD_create.restype = POINTER(DataObject)

    lib.CDC_ALM_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_uint32,  # uint32_t wpOptions
        c_bool,  # bool hasOldStatus
    ]
    lib.CDC_ALM_create.restype = POINTER(DataObject)

    lib.CDC_CTE_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_uint32,  # uint32_t wpOptions
        c_bool,  # bool hasHisRs
    ]
    lib.CDC_CTE_create.restype = POINTER(DataObject)

    lib.CDC_TMS_create.argtypes = [
        c_char_p,  # const char* dataObjectName
        POINTER(ModelNode),  # ModelNode* parent
        c_uint32,  # uint32_t options
        c_uint32,  # uint32_t controlOptions
        c_uint32,  # uint32_t wpOptions
        c_bool,  # bool hasHisRs
    ]
    lib.CDC_TMS_create.restype = POINTER(DataObject)
