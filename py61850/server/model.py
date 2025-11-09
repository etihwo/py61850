"""Model API"""

import ctypes
import datetime
from collections.abc import Callable
from enum import Enum, Flag
from typing import TYPE_CHECKING

from ..binding.iec61850.model import DataAttribute as _cDataAttribute
from ..binding.iec61850.model import DataObject as _cDataObject
from ..binding.iec61850.model import IedModel as _cIedModel
from ..binding.iec61850.model import LogicalDevice as _cLogicalDevice
from ..binding.iec61850.model import LogicalNode as _cLogicalNode
from ..binding.iec61850.model import ModelNode as _cModelNode
from ..binding.iec61850.model import SettingGroupControlBlock as _cSettingGroupControlBlock
from ..binding.loader import Wrapper
from ..common import (
    CdcControlModelOptions,
    CdcOptions,
    Dbpos,
    FunctionalConstraint,
    MmsValue,
    Quality,
    ReportOptions,
    ReportTriggerOptions,
    SampledValueOptions,
    SVSmpMod,
    Timestamp,
    extra_cdc_options,
)
from ..helper import (
    convert_to_bytes,
    convert_to_datetime,
    convert_to_str,
    convert_to_uint64,
)

__all__ = []


if TYPE_CHECKING:
    Pointer = ctypes._Pointer
    IedModelPointer = ctypes._Pointer[_cIedModel]
    ModelNodePointer = ctypes._Pointer[_cModelNode]
    LogicalDevicePointer = ctypes._Pointer[_cLogicalDevice]
    LogicalNodePointer = ctypes._Pointer[_cLogicalNode]
    DataObjectPointer = ctypes._Pointer[_cDataObject]
    DataAttributePointer = ctypes._Pointer[_cDataAttribute]
    SGCBPointer = ctypes._Pointer[_cSettingGroupControlBlock]

else:
    Pointer = ctypes.POINTER
    IedModelPointer = ctypes.POINTER(_cIedModel)
    ModelNodePointer = ctypes.POINTER(_cModelNode)
    LogicalDevicePointer = ctypes.POINTER(_cLogicalDevice)
    LogicalNodePointer = ctypes.POINTER(_cLogicalNode)
    DataObjectPointer = ctypes.POINTER(_cDataObject)
    DataAttributePointer = ctypes.POINTER(_cDataAttribute)
    SGCBPointer = ctypes.POINTER(_cSettingGroupControlBlock)


class DataAttributeType(Enum):
    """Represent the type of a ``DataAttribute``"""

    UNKNOWN_TYPE = -1
    BOOLEAN = 0
    """int"""
    INT8 = 1
    """int8_t"""
    INT16 = 2
    """int16_t"""
    INT32 = 3
    """int32_t"""
    INT64 = 4
    """int64_t"""
    INT128 = 5
    """no native mapping!"""
    INT8U = 6
    """uint8_t"""
    INT16U = 7
    """uint16_t"""
    INT24U = 8
    """uint32_t"""
    INT32U = 9
    """uint32_t"""
    FLOAT32 = 10
    """float"""
    FLOAT64 = 11
    """double"""
    ENUMERATED = 12
    OCTET_STRING_64 = 13
    OCTET_STRING_6 = 14
    OCTET_STRING_8 = 15
    VISIBLE_STRING_32 = 16
    VISIBLE_STRING_64 = 17
    VISIBLE_STRING_65 = 18
    VISIBLE_STRING_129 = 19
    VISIBLE_STRING_255 = 20
    UNICODE_STRING_255 = 21
    TIMESTAMP = 22
    QUALITY = 23
    CHECK = 24
    CODEDENUM = 25
    GENERIC_BITSTRING = 26
    CONSTRUCTED = 27
    ENTRY_TIME = 28
    PHYCOMADDR = 29
    CURRENCY = 30
    OPTFLDS = 31
    """bit-string(10)"""
    TRGOPS = 32
    """bit-string(6)"""


class DataAttributeTriggerOptions(Flag):
    TRG_OPT_DATA_CHANGED = 1
    TRG_OPT_QUALITY_CHANGED = 2
    TRG_OPT_DATA_UPDATE = 4


class ModelNodeType(Enum):
    """Represent the type of a ``ModelNode``"""

    LOGICAL_DEVICE = 0
    """Logical device"""

    LOGICAL_NODE = 1
    """Logical node"""

    DATA_OBJECT = 2
    """Data object"""

    DATA_ATTRIBUTE = 3
    """Data attribute"""


class CheckHandlerResult(Enum):
    """Result code for ``ControlPerformCheckHandler``"""

    ACCEPTED = -1
    """check passed"""
    WAITING_FOR_SELECT = 0
    """select operation in progress - handler will be called again later"""
    HARDWARE_FAULT = 1
    """check failed due to hardware fault"""
    TEMPORARILY_UNAVAILABLE = 2
    """control is already selected or operated"""
    OBJECT_ACCESS_DENIED = 3
    """check failed due to access control reason - access denied for this client or state"""

    OBJECT_UNDEFINED = 4
    """object not visible in this security context ???"""
    VALUE_INVALID = 11
    """ctlVal out of range"""


class ControlHandlerResult(Enum):
    """Result codes for control handler (``ControlWaitForExecutionHandler`` and ``ControlHandler``)"""

    FAILED = 0
    """check or operation failed"""
    OK = 1
    """check or operation was successful"""
    WAITING = 2
    """check or operation is in progress"""


class SelectStateChangedReason(Enum):
    """Reason why a select state of a control object changed"""

    SELECTED = 0
    """control has been selected"""
    CANCELED = 1
    """cancel received for the control"""
    TIMEOUT = 2
    """unselected due to timeout (sboTimeout)"""
    OPERATED = 3
    """unselected due to successful operate"""
    OPERATE_FAILED = 4
    """unselected due to failed operate"""
    DISCONNECTED = 5
    """unselected due to disconnection of selecting client"""


class AccessPolicy(Enum):
    ALLOW = 0
    DENY = 1


class IedModel:
    """IedModel object is the root node of an IEC 61850 data model"""

    def __init__(self, name: str | bytes) -> None:
        name = convert_to_bytes(name)
        handle = Wrapper.lib.IedModel_create(name)
        if not handle:
            raise RuntimeError(f"Failed to create IedModel '{convert_to_str(name)}'")
        self._internal_init(handle)

    def _internal_init(self, handle: IedModelPointer):
        self._handle = handle
        self._model_nodes: dict[int, "ModelNode"] = {}
        self._sgcbs: dict[int, "SettingGroupControlBlock"] = {}

    # def __del__(self):
    #     if hasattr(self, "_handle") and self._handle:
    #         Wrapper.lib.IedModel_destroy(self._handle)

    @staticmethod
    def create_from_config_file(filename: str | bytes) -> "IedModel":
        """Helper function to create an ``IedModel`` from a confg file

        Parameters
        ----------
        filename : str | bytes
            Path of the config file

        Returns
        -------
        IedModel
            IedModel

        Raises
        ------
        RuntimeError
            _description_
        """
        filename = convert_to_bytes(filename)
        handle = Wrapper.lib.ConfigFileParser_createModelFromConfigFileEx(filename)
        if not handle:
            raise RuntimeError(
                f"Failed to create IedModel from the file '{convert_to_str(filename)}'"
            )
        obj = object.__new__(IedModel)
        obj._internal_init(handle)
        return obj

    def create_logical_device(
        self,
        inst: str | bytes,
        name: str | bytes | None = None,
    ) -> "LogicalDevice":
        """Create a logical device in the IedModel

        Parameters
        ----------
        inst : str | bytes
            inst of the logical device
        name : str | bytes | None, optional
            Optional loigcal device name, by default None

        Returns
        -------
        LogicalDevice
            LogicalDevice created

        Raises
        ------
        RuntimeError
            _description_
        """

        inst = convert_to_bytes(inst)
        if name is not None:
            name = convert_to_bytes(name)
        handle = Wrapper.lib.LogicalDevice_createEx(inst, self._handle, name)
        if not handle:
            raise RuntimeError(f"Failed to create LogicalDevice '{convert_to_str(inst)}'")
        return LogicalDevice(handle, self)

    @property
    def handle(self) -> IedModelPointer:
        """Pointer to the underlying C structure"""
        return self._handle

    def logical_device_by_instance(self, ld_inst: str | bytes) -> "LogicalDevice | None":
        """Lookup logical device (LD) by device instance name

        Parameters
        ----------
        ld_inst : str | bytes
            Logical device instance name

        Returns
        -------
        LogicalDevice | None
            Return the LogicalDevice or None if the instance is not found
        """
        ld_inst = convert_to_bytes(ld_inst)
        handle = Wrapper.lib.IedModel_getDeviceByInst(self._handle, ld_inst)
        if handle:
            return LogicalDevice(handle, self)
        return None

    @property
    def name(self) -> bytes:
        """Name of the ``IedModel``"""
        return self._handle.contents.name

    @name.setter
    def name(self, new_name: str | bytes):
        new_name = convert_to_bytes(new_name)
        Wrapper.lib.IedModel_setIedNameForDynamicModel(self._handle, new_name)

    def _try_create_model_node(self, handle) -> "ModelNode | None":
        if handle:
            modeltype = ModelNodeType(handle.contents.modelType)
            if modeltype == ModelNodeType.LOGICAL_DEVICE:
                return LogicalDevice(handle, self)
            if modeltype == ModelNodeType.LOGICAL_NODE:
                return LogicalNode(handle, self)
            if modeltype == ModelNodeType.DATA_OBJECT:
                return DataObject(handle, self)
            if modeltype == ModelNodeType.DATA_ATTRIBUTE:
                return DataAttribute(handle, self)
        return None

    def model_node_by_reference(self, obj_ref: str | bytes) -> "ModelNode | None":
        """Lookup a model node by its object reference.

        This function uses the full logical device reference as part of
        the object reference. E.g. if IED name is "IED1" and the logical
        device instance "WD1" the resulting LD name would be "IED1WD1".
        However if the optional ldName is set then this attribute is used.

        Parameters
        ----------
        obj_ref : str | bytes
            Reference of the object

        Returns
        -------
        ModelNode | None
            ModelNode instance or None if model node does not exist
        """
        obj_ref = convert_to_bytes(obj_ref)
        handle = Wrapper.lib.IedModel_getModelNodeByObjectReference(self._handle, obj_ref)
        return self._try_create_model_node(handle)

    def model_node_by_short_reference(self, obj_ref: str | bytes) -> "ModelNode | None":
        """Lookup a model node by its short reference.

        This version uses the object reference that does not contain the
        IED name or functional name as part of the logical device name.
        Instead the LD part consists of the LD instance name ("inst"
        attribute).

        Parameters
        ----------
        obj_ref : str | bytes
            Reference of the object

        Returns
        -------
        ModelNode | None
            ModelNode instance or None if model node does not exist
        """
        obj_ref = convert_to_bytes(obj_ref)
        handle = Wrapper.lib.IedModel_getModelNodeByShortObjectReference(
            self._handle,
            obj_ref,
        )
        return self._try_create_model_node(handle)


class ModelNode:
    """Base model for ``LogicalDevice``, ``LogicalNode``, ``DataObject``, ``DataAttribute``"""

    def __init__(self, handle: ModelNodePointer, parent: "ModelNode | IedModel") -> None:
        self._handle = handle
        self._parent = parent

    @property
    def handle(self) -> ModelNodePointer:
        """Pointer to the underlying C structure"""
        return self._handle

    @property
    def addressof(self) -> int:
        return ctypes.addressof(self._handle.contents)

    @property
    def name(self) -> bytes:
        """Name of the node"""
        return self._handle.contents.name

    @property
    def model_type(self) -> ModelNodeType:
        """Type of the node"""
        return ModelNodeType(self._handle.contents.modelType)

    @property
    def ied_model(self) -> IedModel:
        """Reference to the ``IedModel`` where the node belongs"""
        if isinstance(self, LogicalDevice):
            return self.ied_model
        assert isinstance(self._parent, ModelNode)
        return self._parent.ied_model

    def child(self, obj_ref: str | bytes) -> "ModelNode | None":
        """Lookup a child by its object reference.

        Parameters
        ----------
        obj_ref : str | bytes
            Reference of the object

        Returns
        -------
        ModelNode | None
            ModelNode instance or None if model node does not exist
        """
        obj_ref = convert_to_bytes(obj_ref)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.ModelNode_getChild(model_node_ptr, obj_ref)

        if handle:
            modeltype = ModelNodeType(handle.contents.modelType)
            if modeltype == ModelNodeType.LOGICAL_NODE:
                return LogicalNode(handle, self)
            if modeltype == ModelNodeType.DATA_OBJECT:
                return DataObject(handle, self)
            if modeltype == ModelNodeType.DATA_ATTRIBUTE:
                return DataAttribute(handle, self)
        return None


class LogicalDevice(ModelNode):
    """LogicalDevice according IEC 61850"""

    def __init__(self, handle: LogicalDevicePointer, ied_model: "IedModel") -> None:
        super().__init__(handle, ied_model)  # type:ignore
        self._handle = ctypes.cast(self._handle, ctypes.POINTER(_cLogicalDevice))
        self._ied_model = ied_model

    @property
    def ld_name(self) -> bytes | None:
        """Return the optional ldName attribute"""
        return self._handle.contents.ldName

    @property
    def ied_model(self) -> IedModel:
        """Reference to the ``IedModel`` where the node belongs"""
        return self._ied_model

    def create_logical_node(self, name: str | bytes) -> "LogicalNode":
        """Create a logcail node in the logical device

        Parameters
        ----------
        name : str | bytes
            Name of the logical node

        Returns
        -------
        LogicalNode
            LogicalNode created

        Raises
        ------
        RuntimeError
            _description_
        """
        name = convert_to_bytes(name)

        handle = Wrapper.lib.LogicalNode_create(name, self._handle)
        if not handle:
            raise RuntimeError(f"Failed to create LogicalNode '{convert_to_str(name)}'")
        return LogicalNode(handle, self)

    def LogicalDevice_getSettingGroupControlBlock(self):
        return Wrapper.lib.LogicalDevice_getSettingGroupControlBlock(self._handle)


class _LogicalNodeOrDataObject(ModelNode):
    """Private class to be used as base class for LogicalNode and DataObject"""

    ####################################################
    # Common Data Classes (CDC)
    ####################################################

    @extra_cdc_options(CdcOptions.PICS_SUBST, CdcOptions.BLK_ENA)
    def create_cdc_sps(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_SPS_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.PICS_SUBST, CdcOptions.BLK_ENA)
    def create_cdc_dps(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_DPS_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.PICS_SUBST, CdcOptions.BLK_ENA)
    def create_cdc_ins(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_INS_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.PICS_SUBST, CdcOptions.BLK_ENA)
    def create_cdc_ens(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ENS_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.FROZEN_VALUE, CdcOptions.UNIT)
    def create_cdc_bcr(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_BCR_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.PICS_SUBST, CdcOptions.BLK_ENA)
    def create_cdc_vss(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_VSS_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.ADDR, CdcOptions.ADDINFO)
    def create_cdc_sec(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_SEC_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.INST_MAG, CdcOptions.RANGE)
    def create_cdc_mv(
        self,
        name: str | bytes,
        is_integer_not_float: bool,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_MV_create(
            name, model_node_ptr, additional_options.value, is_integer_not_float
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.INST_MAG, CdcOptions.RANGE, CdcOptions.RANGE_ANG)
    def create_cdc_cmv(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_CMV_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    @extra_cdc_options(CdcOptions.UNIT, CdcOptions.AC_SCAV, CdcOptions.MIN, CdcOptions.MAX)
    def create_cdc_sav(
        self,
        name: str | bytes,
        is_integer_not_float: bool,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_SAV_create(
            name, model_node_ptr, additional_options.value, is_integer_not_float
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_lpl(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_LPL_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_hst(
        self,
        name: str | bytes,
        maxPts: int,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_HST_create(name, model_node_ptr, additional_options.value, maxPts)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_acd(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ACD_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_act(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ACT_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_spg(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_SPG_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_vsg(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_VSG_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_eng(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ENG_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_ing(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ING_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_asg(
        self,
        name: str | bytes,
        is_integer_not_float: bool,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ASG_create(
            name, model_node_ptr, additional_options.value, is_integer_not_float
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_wye(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_WYE_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_del(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_DEL_create(name, model_node_ptr, additional_options.value)
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    ####################################################
    # Controls
    ####################################################

    def create_cdc_spc(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_SPC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_dpc(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_DPC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_inc(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_INC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_enc(
        self,
        name: str | bytes,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ENC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_bsc(
        self,
        name: str | bytes,
        hasTransientIndicator: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_BSC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            hasTransientIndicator,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_isc(
        self,
        name: str | bytes,
        hasTransientIndicator: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ISC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            hasTransientIndicator,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_apc(
        self,
        name: str | bytes,
        is_integer_not_float: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_APC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            is_integer_not_float,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_bac(
        self,
        name: str | bytes,
        is_integer_not_float: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_BAC_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            is_integer_not_float,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_spv(
        self,
        name: str | bytes,
        wpOptions,
        hasChaManRs: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_SPV_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            wpOptions,
            hasChaManRs,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_stv(
        self,
        name: str | bytes,
        wpOptions,
        hasOldStatus: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_STV_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            wpOptions,
            hasOldStatus,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_cmd(
        self,
        name: str | bytes,
        wpOptions,
        hasOldStatus: bool,
        hasCmTm: bool,
        hasCmCt: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_CMD_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            wpOptions,
            hasOldStatus,
            hasCmTm,
            hasCmCt,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_alm(
        self,
        name: str | bytes,
        wpOptions,
        hasOldStatus: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_ALM_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            wpOptions,
            hasOldStatus,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_cte(
        self,
        name: str | bytes,
        wpOptions,
        hasHisRs: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_CTE_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            wpOptions,
            hasHisRs,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)

    def create_cdc_tms(
        self,
        name: str | bytes,
        wpOptions,
        hasHisRs: bool,
        additional_options: CdcOptions = CdcOptions(0),
        control_options: CdcControlModelOptions = CdcControlModelOptions.MODEL_NONE,
    ) -> "DataObject":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CDC_TMS_create(
            name,
            model_node_ptr,
            additional_options.value,
            control_options.value,
            wpOptions,
            hasHisRs,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataObject '{convert_to_str(name)}'")
        return DataObject(handle, self)


class LogicalNode(_LogicalNodeOrDataObject):
    """LogicalNode according IEC 61850"""

    def __init__(self, handle: ModelNodePointer, parent: ModelNode | IedModel) -> None:
        super().__init__(handle, parent)
        self._handle = ctypes.cast(self._handle, ctypes.POINTER(_cLogicalNode))

    def create_setting_group_control_block(
        self, act_sg: int, num_of_sg: int
    ) -> "SettingGroupControlBlock":
        """Create a setting group control block (SGCB) in the logical node

        The function does not check if the setting group control block is
        created in the LLN0 or in another node. According IEC61850, it
        should be only in LLN0.

        Parameters
        ----------
        act_sg : int
            Active setting group on server startup
        num_of_sg : int
            Number of setting groups

        Returns
        -------
        SettingGroupControlBlock
            Setting group control block created

        Raises
        ------
        RuntimeError
            _description_
        """
        handle = Wrapper.lib.SettingGroupControlBlock_create(self._handle, act_sg, num_of_sg)
        if not handle:
            raise RuntimeError("Failed to create SettingGroupControlBlock")
        return SettingGroupControlBlock(handle)

    def create_dataset(self, name: str | bytes) -> "Dataset":
        """Create a dataset in the logical node

        Parameters
        ----------
        name : str | bytes
            Name of the dataset

        Returns
        -------
        Dataset
            Dataset created

        Raises
        ------
        RuntimeError
            _description_
        """
        name = convert_to_bytes(name)
        handle = Wrapper.lib.DataSet_create(name, self._handle)
        if not handle:
            raise RuntimeError(f"Failed to create Dataset '{convert_to_str(name)}'")

        return Dataset(handle)

    def create_report_control_block(
        self,
        name: str | bytes,
        rpt_id: str | bytes,
        is_buffered: bool,
        dataset_name: str | bytes | None = None,
        conf_ref: int = 1,
        trg_ops: ReportTriggerOptions = ReportTriggerOptions.DATA_CHANGED
        | ReportTriggerOptions.INTEGRITY
        | ReportTriggerOptions.GI,
        rpt_options: ReportOptions = ReportOptions.SEQ_NUM
        | ReportOptions.TIME_STAMP
        | ReportOptions.REASON_FOR_INCLUSION
        | ReportOptions.DATA_SET
        | ReportOptions.BUFFER_OVERFLOW
        | ReportOptions.ENTRY_ID
        | ReportOptions.CONF_REV,
        buf_tm: int = 50,
        intg_pd: int = 90000,
    ) -> "ReportControlBlock":
        """Create a report control block (BRCB or URCB) in the logical node

        Parameters
        ----------
        name : str | bytes
            Name of the report control block
        rpt_id : str | bytes
            _description_
        is_buffered : bool
            True for a buffered RCB - False for unbuffered RCB
        dataset_name : str | bytes | None, optional
            Name of the dataset or None if no dataset is assigned to the
            RCB, by default None
        conf_ref : int, optional
            Configuration revision, by default 1
        trg_ops : TrgOps, optional
            Initial value trigger options, by default TrgOps.DATA_CHANGED
            | TrgOps.INTEGRITY | TrgOps.GI
        rpt_options : ReportOptions, optional
            Initial value for inclusion options. Specifies what elements
            are included in a report, by default ReportOptions.SEQ_NUM |
            ReportOptions.TIME_STAMP | ReportOptions.REASON_FOR_INCLUSION
            | ReportOptions.DATA_SET | ReportOptions.BUFFER_OVERFLOW |
            ReportOptions.ENTRY_ID | ReportOptions.CONF_REV
        buf_tm : int, optional
            Initial value for buffering time of the RCB in milliseconds
            (time between the first event and the preparation of the
            report), by default 50
        intg_pd : int, optional
            Initial value for integrity period in milliseconds, by default 90000

        Returns
        -------
        ReportControlBlock
            Report control block created

        Raises
        ------
        RuntimeError
            _description_
        """
        name = convert_to_bytes(name)
        rpt_id = convert_to_bytes(rpt_id)
        handle = Wrapper.lib.ReportControlBlock_create(
            name,
            self._handle,
            rpt_id,
            is_buffered,
            dataset_name,
            conf_ref,
            trg_ops.value,
            rpt_options.value,
            buf_tm,
            intg_pd,
        )
        if not handle:
            raise RuntimeError(f"Failed to create ReportControlBlock '{convert_to_str(name)}'")
        return ReportControlBlock(handle)

    def create_goose_control_block(
        self,
        name: str | bytes,
        app_id: str | bytes,
        dataset_name: str | bytes | None = None,
        conf_ref: int = 1,
        min_time: int = 200,
        max_time: int = 3000,
        # fixed_offs: bool,
    ) -> "GooseControlBlock":
        """Create a goose control block (GoCB) in the logical node

        Parameters
        ----------
        name : str | bytes
            Name of the GoCB
        app_id : str | bytes
            Application ID of the GoCB
        dataset_name : str | bytes | None, optional
            Name of the dataset or None if no dataset is assigned to the
            GoCB, by default None
        conf_ref : int, optional
            Configuration revision, by default 1
        min_time : int, optional
            Minimum GOOSE retransmission time, by default 200
        max_time : int, optional
            Maximum GOOSE retransmission time, by default 3000

        Returns
        -------
        GooseControlBlock
            Goose control block created

        Raises
        ------
        RuntimeError
            _description_
        """

        name = convert_to_bytes(name)
        app_id = convert_to_bytes(app_id)
        if dataset_name is not None:
            dataset_name = convert_to_bytes(dataset_name)
        handle = Wrapper.lib.GSEControlBlock_create(
            name,
            self.handle,
            app_id,
            dataset_name,
            conf_ref,
            False,  # Not supported
            min_time,
            max_time,
        )
        if not handle:
            raise RuntimeError(f"Failed to create GooseControlBlock '{convert_to_str(name)}'")
        return GooseControlBlock(handle)

    def create_sv_control_block(
        self,
        name: str | bytes,
        sv_id: str | bytes,
        dataset_name: str | bytes | None = None,
        conf_ref: int = 1,
        smp_mod: SVSmpMod = SVSmpMod.SAMPLES_PER_PERIOD,
        smp_rate: int = 80,
        opt_flds: SampledValueOptions = SampledValueOptions(0),
        is_unicast=False,
    ) -> "SVControlBlock":
        """Create a multicast or unicast Sampled Value (SV) control block (SvCB)

        Parameters
        ----------
        name : str | bytes
            Name of the SvCB
        sv_id : str | bytes
            application ID of the SvCB
        dataset_name : str | bytes | None, optional
            Name of the dataset or None if no dataset is assigned to the
            SvCB, by default None
        conf_ref : int, optional
            Configuration revision, by default 1
        smp_mod : SVSmpMod, optional
            Sampling mode, by default SVSmpMod.SAMPLES_PER_PERIOD
        smp_rate : int, optional
            Sampled rate, by default 80
        opt_flds : SampledValueOptions, optional
            Optional fields, by default SampledValueOptions(0)
        is_unicast : bool, optional
            True for a unicast sampled value - False for maluticast
            sampled value, by default False

        Returns
        -------
        SVControlBlock
            Sampled value control block created

        Raises
        ------
        RuntimeError
            _description_
        """
        name = convert_to_bytes(name)
        sv_id = convert_to_bytes(sv_id)
        if dataset_name is not None:
            dataset_name = convert_to_bytes(dataset_name)
        handle = Wrapper.lib.SVControlBlock_create(
            name,
            self._handle,
            name,
            sv_id,
            dataset_name,
            conf_ref,
            smp_mod.value,
            smp_rate,
            opt_flds.value,
            is_unicast,
        )

        if not handle:
            raise RuntimeError(f"Failed to create SVControlBlock '{convert_to_str(name)}'")
        return SVControlBlock(handle)


class DataObject(_LogicalNodeOrDataObject):
    """DataObject according IEC 61850"""

    def __init__(self, handle: ModelNodePointer, parent: ModelNode | IedModel) -> None:
        super().__init__(handle, parent)
        self._handle = ctypes.cast(self._handle, ctypes.POINTER(_cDataObject))

    def child_with_fc(
        self,
        obj_ref: str | bytes,
        fc: FunctionalConstraint,
    ) -> "DataAttribute | None":
        """Lookup a child by its object reference and functional constraint

        Parameters
        ----------
        obj_ref : str | bytes
            _description_
        fc : FunctionalConstraint
            _description_

        Returns
        -------
        DataAttribute | None
            _description_
        """
        obj_ref = convert_to_bytes(obj_ref)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.ModelNode_getChildWithFc(model_node_ptr, obj_ref, fc.value)

        if handle:
            return DataAttribute(handle, self)

        return None

    ####################################################
    # Constructed Attribute Classes (CAC)
    ####################################################

    def create_cac_analog(
        self,
        name: str | bytes,
        fc: FunctionalConstraint,
        trigger_options: DataAttributeTriggerOptions,
        is_integer_not_float: bool,
    ) -> "DataAttribute":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CAC_AnalogueValue_create(
            name,
            model_node_ptr,
            fc.value,
            trigger_options.value,
            is_integer_not_float,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataAttribute '{convert_to_str(name)}'")
        return DataAttribute(handle, self)

    def create_cac_val_with_trans(
        self,
        name: str | bytes,
        fc: FunctionalConstraint,
        trigger_options: DataAttributeTriggerOptions,
        has_transient_indicator: bool,
    ) -> "DataAttribute":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CAC_ValWithTrans_create(
            name,
            model_node_ptr,
            fc.value,
            trigger_options.value,
            has_transient_indicator,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataAttribute '{convert_to_str(name)}'")
        return DataAttribute(handle, self)

    def create_cac_vector(
        self,
        name: str | bytes,
        fc: FunctionalConstraint,
        trigger_options: DataAttributeTriggerOptions,
        options,
    ) -> "DataAttribute":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CAC_Vector_create(
            name,
            model_node_ptr,
            options,
            fc.value,
            trigger_options.value,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataAttribute '{convert_to_str(name)}'")
        return DataAttribute(handle, self)

    def create_cac_point(
        self,
        name: str | bytes,
        fc: FunctionalConstraint,
        trigger_options: DataAttributeTriggerOptions,
        has_z_val: bool,
    ) -> "DataAttribute":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CAC_Point_create(
            name,
            model_node_ptr,
            fc.value,
            trigger_options.value,
            has_z_val,
        )
        if not handle:
            raise RuntimeError(f"Failed to create DataAttribute '{convert_to_str(name)}'")
        return DataAttribute(handle, self)

    def create_cac_scaled_value_config(self, name: str | bytes) -> "DataAttribute":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CAC_ScaledValueConfig_create(name, model_node_ptr)
        if not handle:
            raise RuntimeError(f"Failed to create DataAttribute '{convert_to_str(name)}'")
        return DataAttribute(handle, self)

    def create_cac_unit(
        self,
        name: str | bytes,
        has_magnitude: bool,
    ) -> "DataAttribute":
        name = convert_to_bytes(name)
        model_node_ptr = ctypes.cast(self._handle, ctypes.POINTER(_cModelNode))
        handle = Wrapper.lib.CAC_Unit_create(name, model_node_ptr, has_magnitude)
        if not handle:
            raise RuntimeError(f"Failed to create DataAttribute '{convert_to_str(name)}'")
        return DataAttribute(handle, self)


class DataAttribute(ModelNode):
    """DataAttribute according IEC 61850"""

    def __init__(self, handle: ModelNodePointer, parent: ModelNode | IedModel) -> None:
        super().__init__(handle, parent)
        self._handle = ctypes.cast(self._handle, ctypes.POINTER(_cDataAttribute))

    def init_value(self, value: MmsValue):
        """Set the initial value before the server is started

        Parameters
        ----------
        value : MmsValue
            Value when server will start
        """
        Wrapper.lib.DataAttribute_setValue(self._handle, value.handle)

    @property
    def attribute_type(self) -> DataAttributeType:
        """Type of the data attribute"""
        return DataAttributeType(Wrapper.lib.DataAttribute_getType(self._handle))

    @property
    def trigger_options(self) -> DataAttributeTriggerOptions:
        """Indicate trigger option that can generate an event"""
        return DataAttributeTriggerOptions(Wrapper.lib.DataAttribute_getTrgOps(self._handle))

    @property
    def fc(self) -> FunctionalConstraint:
        """Functional constraint of the data attribute"""
        return FunctionalConstraint(Wrapper.lib.DataAttribute_getFC(self._handle))


class SettingGroupControlBlock:
    """SettingGroupControlBlock according IEC 61850"""

    def __init__(self, handle: SGCBPointer) -> None:
        self._handle = handle

    @property
    def handle(self) -> SGCBPointer:
        """Pointer to the underlying C structure"""
        return self._handle

    @property
    def addressof(self) -> int:
        return ctypes.addressof(self._handle.contents)

    @property
    def act_sg(self) -> int:
        """Active setting group"""
        return self._handle.contents.actSG

    @property
    def num_of_sgs(self) -> int:
        """Number of setting group"""
        return self._handle.contents.numOfSGs

    @property
    def edit_sg(self) -> int:
        """Edited setting group"""
        return self._handle.contents.editSG

    @property
    def cnf_edit(self) -> bool:
        return self._handle.contents.cnfEdit

    @property
    def timestamp(self) -> datetime.datetime:
        value = self._handle.contents.timestamp
        return convert_to_datetime(value)

    @property
    def resv_tms(self) -> int:
        return self._handle.contents.resvTms


class Dataset:
    """Dataset according IEC 61850"""

    def __init__(self, handle) -> None:
        self._handle = handle

    def create_dataset_entry(
        self,
        variable: str | bytes,
        index: int = -1,
        component: str | bytes | None = None,
    ) -> "DatasetEntry":
        """Create an entry in the dataset

        Parameters
        ----------
        variable : str | bytes
            Name of the variable as MMS variable name including FC ("$"
            used as separator), for example TTMP1$MX$TmpSv$instMag$f
        index : int, optional
            Index if the FCDA is an array element, otherwise -1, by
            default -1
        component : str | bytes | None, optional
            Name of the component of the variable if the FCDA is a sub
            element of an array element. If this is not the case then None
            should be given here., by default None

        Returns
        -------
        DatasetEntry
            Dataset entry created

        Raises
        ------
        RuntimeError
            _description_
        """
        variable = convert_to_bytes(variable)
        if component is not None:
            component = convert_to_bytes(component)
        handle = Wrapper.lib.DataSetEntry_create(self._handle, variable, index, component)
        if not handle:
            raise RuntimeError(f"Failed to create DatasetEntry '{convert_to_str(variable)}'")
        return DatasetEntry(handle)

    @property
    def name(self) -> bytes:
        """Name of the dataset"""
        return Wrapper.lib.DataSet_getName(
            self._handle,  # DataSet* self
        ).split(
            b"$"
        )[-1]

    @property
    def size(self) -> int:
        """Number of entry in the dataset"""
        return Wrapper.lib.DataSet_getSize(
            self._handle,  # DataSet* self
        )


class DatasetEntry:
    """Represent an entry in a dataset"""

    def __init__(self, handle) -> None:
        self._handle = handle


class ReportControlBlock:
    """ReportControlBlock according IEC 61850"""

    def __init__(self, handle):
        self._handle = handle


class GooseControlBlock:
    """GooseControlBlock according IEC 61850"""

    def __init__(self, handle):
        self._handle = handle


class SVControlBlock:
    """Multicast or unicast sampled value control block according IEC 61850"""

    def __init__(self, handle):
        self._handle = handle
