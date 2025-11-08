"""Implements function and class relative to goose on client side"""

import ctypes
import datetime
from collections.abc import Callable
from ctypes import byref, c_bool, c_int, c_void_p
from enum import Enum, Flag
from typing import TYPE_CHECKING

from ..binding.iec61850.client import CommandTerminationHandler
from ..binding.iec61850.client import IedClientError as _cIedClientError
from ..binding.iec61850.client import (
    IedClientGetFileHandler,
    IedConnection_ClosedHandler,
    IedConnection_StateChangedHandler,
)
from ..binding.iec61850.client import LastApplError as _cLastApplError
from ..binding.iec61850.client import ReportCallbackFunction
from ..binding.iec61850.client import (
    sClientGooseControlBlock as _sClientGooseControlBlock,
)
from ..binding.iec61850.client import (
    sClientReportControlBlock as _sClientReportControlBlock,
)
from ..binding.loader import Wrapper
from ..common import (
    ACSIClass,
    ControlAddCause,
    ControlLastApplError,
    ControlModel,
    FunctionalConstraint,
    LinkedList,
    MmsType,
    MmsValue,
    OrCat,
    Quality,
    ReportOptions,
    ReportTriggerOptions,
    Timestamp,
)
from ..helper import convert_to_bytes, convert_to_datetime
from .dataset import DataSet

if TYPE_CHECKING:
    GooseControlBlockPointer = ctypes._Pointer[_sClientGooseControlBlock]  # type: ignore
    ReportControlBlockPointer = ctypes._Pointer[_sClientReportControlBlock]  # type: ignore
else:
    GooseControlBlockPointer = ctypes.POINTER(_sClientGooseControlBlock)
    ReportControlBlockPointer = ctypes.POINTER(_sClientReportControlBlock)

if TYPE_CHECKING:
    from .connection import IedConnection


class GocbElement(Flag):
    """Flag to detect goose control block element"""

    GO_ENA = 1
    """Enable GOOSE publisher GoCB block element"""
    GO_ID = 2
    """GOOSE ID GoCB block element"""
    DATSET = 4
    """Data set GoCB block element"""
    CONF_REV = 8
    """Configuration revision GoCB block element (this is usually read-only)"""
    NDS_COMM = 16
    """Need commission GoCB block element (read-only according to 61850-7-2)"""
    DST_ADDRESS = 32
    """Destination address GoCB block element (read-only according to 61850-7-2)"""
    MIN_TIME = 64
    """Minimum time GoCB block element (read-only according to 61850-7-2)"""
    MAX_TIME = 128
    """Maximum time GoCB block element (read-only according to 61850-7-2)"""
    FIXED_OFFS = 256
    """Fixed offsets GoCB block element (read-only according to 61850-7-2)"""
    ALL = 511
    """select all elements of the GoCB"""


class GooseControlBlock:
    """Goose control block"""

    def __init__(self, handle: GooseControlBlockPointer):
        self._handle = handle
        self._element_changed = GocbElement(0)

    def __del__(self):
        Wrapper.lib.ClientGooseControlBlock_destroy(self._handle)

    @property
    def handle(self):
        """Pointer to the underlying C structure"""
        return self._handle

    @property
    def element_changed(self) -> GocbElement:
        return self._element_changed

    def clear_element_changed(self):
        """Reset the flag used to detect which elment has been changed"""
        self._element_changed = GocbElement(0)

    @property
    def reference(self) -> bytes:
        """Reference of the goose control block"""
        return self._handle.contents.objectReference

    @property
    def go_ena(self) -> bool:
        """Indicate whther the goose control block is enabled"""
        return Wrapper.lib.ClientGooseControlBlock_getGoEna(self._handle)

    @go_ena.setter
    def go_ena(self, go_ena: bool):
        self._element_changed |= GocbElement.GO_ENA
        Wrapper.lib.ClientGooseControlBlock_setGoEna(self._handle, go_ena)

    @property
    def go_id(self) -> bytes:
        return Wrapper.lib.ClientGooseControlBlock_getGoID(self._handle)

    @go_id.setter
    def go_id(self, go_id: str | bytes):
        go_id = convert_to_bytes(go_id)
        self._element_changed |= GocbElement.GO_ID
        Wrapper.lib.ClientGooseControlBlock_setGoID(self._handle, go_id)

    @property
    def datset(self) -> bytes:
        return Wrapper.lib.ClientGooseControlBlock_getDatSet(self._handle)

    @datset.setter
    def datset(self, datset: str | bytes):
        datset = convert_to_bytes(datset)
        self._element_changed |= GocbElement.DATSET
        Wrapper.lib.ClientGooseControlBlock_setDatSet(self._handle, datset)

    @property
    def conf_ref(self) -> int:
        return Wrapper.lib.ClientGooseControlBlock_getConfRev(self._handle)

    @property
    def nds_comm(self) -> bool:
        return Wrapper.lib.ClientGooseControlBlock_getNdsComm(self._handle)

    @property
    def min_time(self) -> int:
        return Wrapper.lib.ClientGooseControlBlock_getMinTime(self._handle)

    @property
    def max_time(self) -> int:
        return Wrapper.lib.ClientGooseControlBlock_getMaxTime(self._handle)

    @property
    def fixed_offset(self) -> bool:
        return Wrapper.lib.ClientGooseControlBlock_getFixedOffs(self._handle)

    # def ClientGooseControlBlock_getDstAddress(self) -> PhyComAddress:
    #     return Wrapper.lib.ClientGooseControlBlock_getDstAddress.argtypes = [
    #         ClientGooseControlBlock,  # ClientGooseControlBlock self
    #     ]
    #     lib.ClientGooseControlBlock_getDstAddress.restype = PhyComAddress

    # def ClientGooseControlBlock_setDstAddress(self, value: PhyComAddress):
    #     Wrapper.lib.ClientGooseControlBlock_setDstAddress.argtypes = [
    #         ClientGooseControlBlock,  # ClientGooseControlBlock self
    #         PhyComAddress,  # PhyComAddress value
    #     ]
