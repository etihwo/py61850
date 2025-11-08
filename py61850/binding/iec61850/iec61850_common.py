"""Module for C binding with iec61850/inc/iec61850_common.h"""

from ctypes import (
    CDLL,
    POINTER,
    Structure,
    Union,
    c_bool,
    c_char_p,
    c_float,
    c_int,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
)

from ..mms import MmsValue


class PhyComAddress(Structure):
    _fields_ = [
        ("vlanPriority", c_uint8),
        ("vlanId", c_uint16),
        ("appId", c_uint16),
        ("dstAddress", c_uint8 * 6),
    ]


class Timestamp(Union):
    _fields_ = [("val", c_uint8 * 8)]


ACSIClass = c_int
ControlModel = c_int
ControlAddCause = c_int
ControlLastApplError = c_int
FunctionalConstraint = c_int
Dbpos = c_int

Quality = c_uint16
Validity = c_uint16

nsSinceEpoch = c_uint64
msSinceEpoch = c_uint64


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    lib.Timestamp_create.argtypes = []
    lib.Timestamp_create.restype = POINTER(Timestamp)

    lib.Timestamp_createFromByteArray.argtypes = [
        POINTER(c_uint8),  # const uint8_t* byteArray
    ]
    lib.Timestamp_createFromByteArray.restype = POINTER(Timestamp)

    lib.Timestamp_destroy.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_destroy.restype = None

    lib.Timestamp_clearFlags.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_clearFlags.restype = None

    lib.Timestamp_getTimeInSeconds.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_getTimeInSeconds.restype = c_uint32

    lib.Timestamp_getTimeInMs.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_getTimeInMs.restype = msSinceEpoch

    lib.Timestamp_getTimeInNs.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_getTimeInNs.restype = nsSinceEpoch

    lib.Timestamp_isLeapSecondKnown.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_isLeapSecondKnown.restype = c_bool

    lib.Timestamp_setLeapSecondKnown.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        c_bool,  # bool value
    ]
    lib.Timestamp_setLeapSecondKnown.restype = None

    lib.Timestamp_hasClockFailure.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_hasClockFailure.restype = c_bool

    lib.Timestamp_setClockFailure.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        c_bool,  # bool value
    ]
    lib.Timestamp_setClockFailure.restype = None

    lib.Timestamp_isClockNotSynchronized.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_isClockNotSynchronized.restype = c_bool

    lib.Timestamp_setClockNotSynchronized.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        c_bool,  # bool value
    ]
    lib.Timestamp_setClockNotSynchronized.restype = None

    lib.Timestamp_getSubsecondPrecision.argtypes = [
        POINTER(Timestamp),
    ]  # Timestamp* self
    lib.Timestamp_getSubsecondPrecision.restype = c_int

    lib.Timestamp_setFractionOfSecondPart.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        c_uint32,  # uint32_t fractionOfSecond
    ]
    lib.Timestamp_setFractionOfSecondPart.restype = None

    lib.Timestamp_getFractionOfSecondPart.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_getFractionOfSecondPart.restype = c_uint32

    lib.Timestamp_getFractionOfSecond.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
    ]
    lib.Timestamp_getFractionOfSecond.restype = c_float

    lib.Timestamp_setSubsecondPrecision.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        c_int,  # int subsecondPrecision
    ]
    lib.Timestamp_setSubsecondPrecision.restype = None

    lib.Timestamp_setTimeInSeconds.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        c_uint32,  # uint32_t secondsSinceEpoch
    ]
    lib.Timestamp_setTimeInSeconds.restype = None

    lib.Timestamp_setTimeInMilliseconds.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        msSinceEpoch,  # msSinceEpoch msTime
    ]
    lib.Timestamp_setTimeInMilliseconds.restype = None

    lib.Timestamp_setTimeInNanoseconds.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        nsSinceEpoch,  # nsSinceEpoch nsTime
    ]
    lib.Timestamp_setTimeInNanoseconds.restype = None

    lib.Timestamp_setByMmsUtcTime.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        POINTER(MmsValue),  # const MmsValue* mmsValue
    ]
    lib.Timestamp_setByMmsUtcTime.restype = None

    lib.Timestamp_toMmsValue.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        POINTER(MmsValue),  # MmsValue* mmsValue
    ]
    lib.Timestamp_toMmsValue.restype = POINTER(MmsValue)

    lib.Timestamp_fromMmsValue.argtypes = [
        POINTER(Timestamp),  # Timestamp* self
        POINTER(MmsValue),  # MmsValue* mmsValue
    ]
    lib.Timestamp_fromMmsValue.restype = POINTER(Timestamp)

    lib.LibIEC61850_getVersionString.argtypes = []
    lib.LibIEC61850_getVersionString.restype = c_char_p
