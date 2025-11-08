"""Implements function and class relative to report and report control block on client side"""

import ctypes
import datetime
from collections.abc import Callable
from ctypes import c_int, c_void_p
from enum import Flag
from typing import TYPE_CHECKING

from ..binding.iec61850.client import ReportCallbackFunction
from ..binding.iec61850.client import (
    sClientReportControlBlock as _sClientReportControlBlock,
)
from ..binding.loader import Wrapper
from ..common import MmsValue, ReportOptions, ReportTriggerOptions, Timestamp
from ..helper import convert_to_bytes, convert_to_datetime

if TYPE_CHECKING:
    ReportControlBlockPointer = ctypes._Pointer[_sClientReportControlBlock]  # type: ignore
else:
    ReportControlBlockPointer = ctypes.POINTER(_sClientReportControlBlock)

if TYPE_CHECKING:
    from .connection import IedConnection

__all__ = []


class RcbElement(Flag):
    """Flag to detect report control block element"""

    RPT_ID = 1
    """include the report ID into the setRCB request"""
    RPT_ENA = 2
    """include the report enable element into the setRCB request"""
    RESV = 4
    """include the reservation element into the setRCB request (only available in unbuffered RCBs!)"""
    DATSET = 8
    """include the data set element into the setRCB request"""
    CONF_REV = 16
    """include the configuration revision element into the setRCB request"""
    OPT_FLDS = 32
    """include the option fields element into the setRCB request"""
    BUF_TM = 64
    """include the bufTm (event buffering time) element into the setRCB request"""
    SQ_NUM = 128
    """include the sequence number element into the setRCB request (should be used!)"""
    TRG_OPS = 256
    """include the trigger options element into the setRCB request"""
    INTG_PD = 512
    """include the integrity period element into the setRCB request"""
    GI = 1024
    """include the GI (general interrogation) element into the setRCB request"""
    PURGE_BUF = 2048
    """include the purge buffer element into the setRCB request (only available in buffered RCBs)"""
    ENTRY_ID = 4096
    """include the entry ID element into the setRCB request (only available in buffered RCBs)"""
    TIME_OF_ENTRY = 8192
    """include the time of entry element into the setRCB request (only available in buffered RCBs)"""
    RESV_TMS = 16384
    """include the reservation time element into the setRCB request (only available in buffered RCBs)"""
    OWNER = 32768
    """include the owner element into the setRCB request"""


class ReasonForInclusion(Flag):
    """Describes the reason for the inclusion of the element in the report"""

    NOT_INCLUDED = 0
    """the element is not included in the received report"""
    DATA_CHANGE = 1
    """the element is included due to a change of the data value"""
    QUALITY_CHANGE = 2
    """the element is included due to a change in the quality of data"""
    DATA_UPDATE = 4
    """the element is included due to an update of the data value"""
    INTEGRITY = 8
    """the element is included due to a periodic integrity report task"""
    GI = 16
    """the element is included due to a general interrogation by the client"""
    UNKNOWN = 32
    """the reason for inclusion is unknown (e.g. report is not configured to include reason-for-inclusion)"""


class Report:
    """Report"""

    def __init__(self, handle: c_void_p) -> None:
        self._handle = handle

    @property
    def has_dataset_name(self) -> bool:
        """Indicate whether dataset name is included in the report"""
        return Wrapper.lib.ClientReport_hasDataSetName(self._handle)

    @property
    def dataset_name(self) -> bytes:
        """Name of the dataset"""
        return Wrapper.lib.ClientReport_getDataSetName(self._handle)

    @property
    def dataset_values(self) -> MmsValue:
        """Received data set values of the report"""
        handle = Wrapper.lib.ClientReport_getDataSetValues(self._handle)
        return MmsValue(handle)

    @property
    def entry_id(self) -> bytearray | None:
        """Entry ID of the report"""
        handle = Wrapper.lib.ClientReport_getEntryId(self._handle)

        if not handle:
            return None
        value = MmsValue(handle)
        return value.to_octet_string()

    @property
    def more_seqments_follow(self) -> bool:
        """True in case this is part of a segmented report and more report
        segments will follow or false, if the current report is not a
        segmented report or is the last segment of a segmented report."""
        return Wrapper.lib.ClientReport_getMoreSeqmentsFollow(self._handle)

    @property
    def rcb_reference(self) -> bytes:
        """Reference (name) of the server RCB associated with this ClientReport object"""
        return Wrapper.lib.ClientReport_getRcbReference(self._handle)

    @property
    def rpt_id(self) -> bytes:
        """RptId of the server RCB associated with this ClientReport object"""
        val = Wrapper.lib.ClientReport_getRptId(self._handle)
        return val

    def has_buf_ovfl(self) -> bool:
        """Indicates if the report contains the bufOvfl (buffer overflow) flag"""
        return Wrapper.lib.ClientReport_hasBufOvfl(self._handle)

    @property
    def buf_ovfl(self) -> bool:
        """Value of the bufOvfl flag"""
        return Wrapper.lib.ClientReport_getBufOvfl(self._handle)

    @property
    def has_conf_rev(self) -> bool:
        """Indicates if the last received report contains the configuration revision"""
        return Wrapper.lib.ClientReport_hasConfRev(self._handle)

    @property
    def conf_rev(self) -> int:
        """Value of the configuration revision"""
        return Wrapper.lib.ClientReport_getConfRev(self._handle)

    @property
    def has_data_reference(self) -> bool:
        """Indicates if the report contains data references for the reported data set members"""
        return Wrapper.lib.ClientReport_hasDataReference(self._handle)

    def get_data_reference(self, element_index: int) -> bytes:
        """Get the data-reference of the element of the report data set

        Parameters
        ----------
        element_index : int
            _description_

        Returns
        -------
        bytes
            _description_
        """
        return Wrapper.lib.ClientReport_getDataReference(self._handle, element_index)

    @property
    def has_reason_for_inclusion(self) -> bool:
        """Indicates if the last received report contains reason-for-inclusion information"""
        return Wrapper.lib.ClientReport_hasReasonForInclusion(self._handle)

    def get_reason_for_inclusion(self, element_index: int) -> ReasonForInclusion:
        """Get the reason code (reason for inclusion) for a specific report data set element

        Parameters
        ----------
        element_index : int
            _description_

        Returns
        -------
        ReasonForInclusion
            _description_
        """
        val = Wrapper.lib.ClientReport_getReasonForInclusion(self._handle, element_index)
        return ReasonForInclusion(val)

    @property
    def has_seq_num(self) -> bool:
        """Indicates if the last received report contains a sequence number"""
        return Wrapper.lib.ClientReport_hasSeqNum(self._handle)

    @property
    def seq_num(self) -> int:
        """Value of the sequence number"""
        return Wrapper.lib.ClientReport_getSeqNum(self._handle)

    @property
    def has_sub_seq_num(self) -> bool:
        """Indicates if the report contains a sub sequence number and a more segments follow flags (for segmented reporting)"""
        return Wrapper.lib.ClientReport_hasSubSeqNum(self._handle)

    @property
    def sub_seq_num(self) -> int:
        """Value of the sub sequence number"""
        return Wrapper.lib.ClientReport_getSubSeqNum(self._handle)

    @property
    def has_timestamp(self) -> bool:
        """Indicates if the last received report contains a timestamp"""
        return Wrapper.lib.ClientReport_hasTimestamp(self._handle)

    @property
    def timestamp(self) -> datetime.datetime:
        """Value of the timestamp"""
        ms = Wrapper.lib.ClientReport_getTimestamp(self._handle)
        return convert_to_datetime(ms)


class ReportControlBlock:
    """Report control block"""

    def __init__(self, handle: ReportControlBlockPointer, ied_connection: "IedConnection"):
        self._handle = handle
        self._element_changed = RcbElement(0)
        self._ied_connection = ied_connection

    @property
    def handle(self):
        """Pointer to the underlying C structure"""
        return self._handle

    @property
    def element_changed(self) -> RcbElement:
        """List of property changed manually"""
        return self._element_changed

    def clear_element_changed(self):
        """Reset the flag used to detect which elment has been changed"""
        self._element_changed = RcbElement(0)

    def on_report(self, callback: Callable[["Report"], None]):
        """Register a report callback function

        Parameters
        ----------
        callback : Callable[["Report"], None]
            _description_
        """
        self._ied_connection.register_report_handler(self.reference, self.rpt_id, callback)

    def subscribe(
        self,
        trg_ops: ReportTriggerOptions | None = None,
        intg_pd: int | None = None,
        opt_flds: ReportOptions | None = None,
    ):
        if opt_flds is not None:
            self.optflds = opt_flds
        if intg_pd is not None:
            self.intg_pd = intg_pd
        if trg_ops is not None:
            self.trg_ops = trg_ops
        self._ied_connection.set_rcb_values(self)
        self.rpt_ena = True
        self._ied_connection.set_rcb_values(self)

    @property
    def reference(self) -> bytes:
        """Reference of the report control block"""
        return Wrapper.lib.ClientReportControlBlock_getObjectReference(self._handle)

    @property
    def is_buffered(self) -> bool:
        """Indicate whether it is a buffered report control block (BRCB) or an unbeffered report control block (URCB)"""
        return Wrapper.lib.ClientReportControlBlock_isBuffered(self._handle)

    @property
    def rpt_id(self) -> bytes:
        """Value of the report id"""
        return Wrapper.lib.ClientReportControlBlock_getRptId(self._handle)

    @rpt_id.setter
    def rpt_id(self, rpt_id: str | bytes):
        rpt_id = convert_to_bytes(rpt_id)
        self._element_changed |= RcbElement.RPT_ID
        Wrapper.lib.ClientReportControlBlock_setRptId(self._handle, rpt_id)

    @property
    def rpt_ena(self) -> bool:
        """Indicate whther the report control block is enabled"""
        return Wrapper.lib.ClientReportControlBlock_getRptEna(self._handle)

    @rpt_ena.setter
    def rpt_ena(self, rpt_ena: bool):
        self._element_changed |= RcbElement.RPT_ENA
        Wrapper.lib.ClientReportControlBlock_setRptEna(self._handle, rpt_ena)

    @property
    def resv(self) -> bool:
        return Wrapper.lib.ClientReportControlBlock_getResv(self._handle)

    @resv.setter
    def resv(self, resv: bool):
        self._element_changed |= RcbElement.RESV
        Wrapper.lib.ClientReportControlBlock_setResv(self._handle, resv)

    @property
    def dataset_reference(self) -> bytes:
        return Wrapper.lib.ClientReportControlBlock_getDataSetReference(self._handle)

    @dataset_reference.setter
    def dataset_reference(self, dataset_reference: str | bytes):
        dataset_reference = convert_to_bytes(dataset_reference)
        self._element_changed |= RcbElement.DATSET
        Wrapper.lib.ClientReportControlBlock_setDataSetReference(self._handle, dataset_reference)

    @property
    def conf_rev(self) -> int:
        """Value of the configuration revision"""
        return Wrapper.lib.ClientReportControlBlock_getConfRev(self._handle)

    @property
    def optflds(self) -> ReportOptions:
        val: c_int = Wrapper.lib.ClientReportControlBlock_getOptFlds(self._handle)
        return ReportOptions(val.value)

    @optflds.setter
    def optflds(self, optflds: ReportOptions):
        self._element_changed |= RcbElement.OPT_FLDS
        Wrapper.lib.ClientReportControlBlock_setOptFlds(self._handle, optflds.value)

    @property
    def buf_tm(self) -> int:
        return Wrapper.lib.ClientReportControlBlock_getBufTm(self._handle)

    @buf_tm.setter
    def buf_tm(self, buf_tm: int):
        self._element_changed |= RcbElement.BUF_TM
        return Wrapper.lib.ClientReportControlBlock_setBufTm(self._handle, buf_tm)

    @property
    def sq_num(self) -> int:
        return Wrapper.lib.ClientReportControlBlock_getSqNum(self._handle)

    @property
    def trg_ops(self) -> ReportTriggerOptions:
        val = Wrapper.lib.ClientReportControlBlock_getTrgOps(self._handle)
        return ReportTriggerOptions(val)

    @trg_ops.setter
    def trg_ops(self, trg_ops: ReportTriggerOptions):
        self._element_changed |= RcbElement.TRG_OPS
        Wrapper.lib.ClientReportControlBlock_setTrgOps(self._handle, trg_ops.value)

    @property
    def intg_pd(self) -> int:
        return Wrapper.lib.ClientReportControlBlock_getIntgPd(self._handle)

    @intg_pd.setter
    def intg_pd(self, intg_pd: int):
        self._element_changed |= RcbElement.INTG_PD
        Wrapper.lib.ClientReportControlBlock_setIntgPd(self._handle, intg_pd)

    @property
    def gi(self) -> bool:
        return Wrapper.lib.ClientReportControlBlock_getGI(self._handle)

    @gi.setter
    def gi(self, gi: bool):
        self._element_changed |= RcbElement.GI
        Wrapper.lib.ClientReportControlBlock_setGI(self._handle, gi)

    @property
    def purge_buf(self) -> bool:
        return Wrapper.lib.ClientReportControlBlock_getPurgeBuf(self._handle)

    @purge_buf.setter
    def purge_buf(self, purge_buf: bool):
        self._element_changed |= RcbElement.PURGE_BUF
        Wrapper.lib.ClientReportControlBlock_setPurgeBuf(self._handle, purge_buf)

    def has_resv_tms(self) -> bool:
        return Wrapper.lib.ClientReportControlBlock_hasResvTms(self._handle)

    @property
    def resv_tms(self) -> int:
        return Wrapper.lib.ClientReportControlBlock_getResvTms(self._handle)

    @resv_tms.setter
    def resv_tms(self, resv_tms: int):
        self._element_changed |= RcbElement.RESV_TMS
        Wrapper.lib.ClientReportControlBlock_setResvTms(self._handle, resv_tms)

    @property
    def entry_id(self) -> MmsValue:
        handle = Wrapper.lib.ClientReportControlBlock_getEntryId(self._handle)
        return MmsValue(handle)

    @entry_id.setter
    def entry_id(self, entry_id: MmsValue):
        self._element_changed |= RcbElement.ENTRY_ID
        Wrapper.lib.ClientReportControlBlock_setEntryId(self._handle, entry_id.handle)

    @property
    def entry_time(self) -> datetime.datetime:
        return Wrapper.lib.ClientReportControlBlock_getEntryTime(self._handle)

    @property
    def owner(self) -> MmsValue:
        handle = Wrapper.lib.ClientReportControlBlock_getOwner(self._handle)
        return MmsValue(handle)
