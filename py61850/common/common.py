import datetime
from enum import Enum, Flag

from ..binding.loader import Wrapper
from ..helper import convert_to_datetime

__all__ = []


class Iec61850Edition(Enum):
    EDITION_1 = 0
    """IEC 61850 edition 1"""

    EDITION_2 = 1
    """IEC 61850 edition 2"""

    EDITION_2_1 = 2
    """IEC 61850 edition 2.1"""


class OrCat(Enum):
    """Category of the originator of the control request"""

    NOT_SUPPORTED = 0
    BAY_CONTROL = 1
    STATION_CONTROL = 2
    REMOTE_CONTROL = 3
    AUTOMATIC_BAY = 4
    AUTOMATIC_STATION = 5
    AUTOMATIC_REMOTE = 6
    MAINTENANCE = 7
    PROCESS = 8


class ACSIClass(Enum):
    """ACSIClass"""

    DATA_OBJECT = 0
    """Data object"""
    DATA_SET = 1
    """Dataset"""
    BRCB = 2
    """Buffered report control block"""
    URCB = 3
    """Unbeffered report control block"""
    LCB = 4
    """Log control block"""
    LOG = 5
    """Log"""
    SGCB = 6
    """Setting group control block"""
    GoCB = 7
    """Goose control block"""
    GsCB = 8
    """GSSE control block"""
    MSVCB = 9
    """Multicast sampled value control block"""
    USVCB = 10
    """Unicast sampled value control block"""


class FunctionalConstraint(Enum):
    # Status information
    ST = 0
    # Measurands - analog values
    MX = 1
    # Setpoint
    SP = 2
    # Substitution
    SV = 3
    # Configuration
    CF = 4
    # Description
    DC = 5
    # Setting group
    SG = 6
    # Setting group editable
    SE = 7
    # Service response / Service tracking
    SR = 8
    # Operate received
    OR = 9
    # Blocking
    BL = 10
    # Extended definition
    EX = 11
    # Control
    CO = 12
    # Unicast SV
    US = 13
    # Multicast SV
    MS = 14
    # Unbuffered report
    RP = 15
    # Buffered report
    BR = 16
    # Log control blocks
    LG = 17
    # Goose control blocks
    GO = 18
    # All FCs - wildcard value
    ALL = 99
    NONE = -1


class Dbpos(Enum):
    INTERMEDIATE_STATE = 0
    OFF = 1
    ON = 2
    BAD_STATE = 3


class SVSmpMod(Enum):
    """For sampled value, indicate how the sample rate is expressed"""

    SAMPLES_PER_PERIOD = 0

    SAMPLES_PER_SECOND = 1

    SECONDS_PER_SAMPLE = 2


class ReportTriggerOptions(Flag):
    # Report will be triggered when data changes */
    DATA_CHANGED = 1
    # Report will be triggered when quality changes */
    QUALITY_CHANGED = 2
    # Report will be triggered when data is updated */
    DATA_UPDATE = 4
    # Report will be triggered periodically */
    INTEGRITY = 8
    # Report will be triggered by GI (general interrogation) request */
    GI = 16
    # Report will be triggered only on rising edge (transient variable */
    TRANSIENT = 128


class ReportOptions(Flag):
    NONE = 0
    SEQ_NUM = 1
    TIME_STAMP = 2
    REASON_FOR_INCLUSION = 4
    DATA_SET = 8
    DATA_REFERENCE = 16
    BUFFER_OVERFLOW = 32
    ENTRY_ID = 64
    CONF_REV = 128
    SEGMENTATION = 256
    ALL = (
        SEQ_NUM
        | TIME_STAMP
        | REASON_FOR_INCLUSION
        | DATA_SET
        | DATA_REFERENCE
        | BUFFER_OVERFLOW
        | ENTRY_ID
        | CONF_REV
        | SEGMENTATION
    )


class SampledValueOptions(Flag):
    """Sampled value optional fields"""

    IEC61850_SV_OPT_REFRESH_TIME = 1
    """SV ASDU contains attribute RefrTm"""

    IEC61850_SV_OPT_SAMPLE_SYNC = 2
    """SV ASDU contains attribute SmpSynch"""

    IEC61850_SV_OPT_SAMPLE_RATE = 4
    """SV ASDU contains attribute SmpRate"""

    IEC61850_SV_OPT_DATA_SET = 8
    """SV ASDU contains attribute DatSet"""

    IEC61850_SV_OPT_SECURITY = 16
    """SV ASDU contains attribute Security"""


class ObjectReference: ...


class PhyComAddress: ...


class QualityValidity(Flag):
    GOOD = 0
    INVALID = 2
    RESERVED = 1
    QUESTIONABLE = 3


class QualityDetail(Flag):
    OVERFLOW = 4
    OUT_OF_RANGE = 8
    BAD_REFERENCE = 16
    OSCILLATORY = 32
    FAILURE = 64
    OLD_DATA = 128
    INCONSISTENT = 256
    INACCURATE = 512


class Quality(Flag):
    VALIDITY_GOOD = 0
    VALIDITY_INVALID = 2
    VALIDITY_RESERVED = 1
    VALIDITY_QUESTIONABLE = 3

    DETAIL_OVERFLOW = 4
    DETAIL_OUT_OF_RANGE = 8
    DETAIL_BAD_REFERENCE = 16
    DETAIL_OSCILLATORY = 32
    DETAIL_FAILURE = 64
    DETAIL_OLD_DATA = 128
    DETAIL_INCONSISTENT = 256
    DETAIL_INACCURATE = 512

    SOURCE_SUBSTITUTED = 1024

    TEST = 2048

    OPERATOR_BLOCKED = 4096

    DERIVED = 8192

    @property
    def validity(self) -> QualityValidity:
        """Validity of the quality value"""
        return QualityValidity(self.value & 0x03)

    @property
    def detail(self) -> QualityDetail:
        """Detail of the quality value"""
        return QualityDetail(self.value & 0x3FC)


class Timestamp:
    def __init__(self, handle) -> None:
        self._handle = handle

    def Timestamp_clearFlags(self):
        Wrapper.lib.Timestamp_clearFlags(self._handle)

    def Timestamp_getTimeInSeconds(self) -> int:
        return Wrapper.lib.Timestamp_getTimeInSeconds(self._handle)

    def get_time(self) -> datetime.datetime:
        val_ms = Wrapper.lib.Timestamp_getTimeInMs(self._handle)
        return convert_to_datetime(val_ms)

    def Timestamp_getTimeInMs(self) -> int:
        return Wrapper.lib.Timestamp_getTimeInMs(self._handle)

    def Timestamp_getTimeInNs(self) -> int:
        return Wrapper.lib.Timestamp_getTimeInNs(self._handle)

    def Timestamp_isLeapSecondKnown(self) -> bool:
        return Wrapper.lib.Timestamp_isLeapSecondKnown(self._handle)

    def Timestamp_setLeapSecondKnown(self, value: bool):
        Wrapper.lib.Timestamp_setLeapSecondKnown(self._handle, value)

    def Timestamp_hasClockFailure(self) -> bool:
        return Wrapper.lib.Timestamp_hasClockFailure(self._handle)

    def Timestamp_setClockFailure(self, value: bool):
        Wrapper.lib.Timestamp_setClockFailure(self._handle, value)

    def Timestamp_isClockNotSynchronized(self) -> bool:
        return Wrapper.lib.Timestamp_isClockNotSynchronized(self._handle)

    def Timestamp_setClockNotSynchronized(self, value: bool):
        Wrapper.lib.Timestamp_setClockNotSynchronized(self._handle, value)

    def Timestamp_getSubsecondPrecision(self) -> int:
        return Wrapper.lib.Timestamp_getSubsecondPrecision(self._handle)

    def Timestamp_setFractionOfSecondPart(self, fractionOfSecond: int):
        Wrapper.lib.Timestamp_setFractionOfSecondPart(self._handle, fractionOfSecond)

    def Timestamp_getFractionOfSecondPart(self) -> int:
        return Wrapper.lib.Timestamp_getFractionOfSecondPart(self._handle)

    def Timestamp_getFractionOfSecond(self) -> float:
        return Wrapper.lib.Timestamp_getFractionOfSecond(self._handle)
