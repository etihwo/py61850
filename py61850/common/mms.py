import ctypes
import datetime
from enum import Enum
from typing import TYPE_CHECKING

from ..binding.loader import Wrapper
from ..binding.mms.mms_value import sMmsValue as _sMmsValue
from ..helper import (
    convert_to_bytes,
    convert_to_datetime,
    convert_to_str,
    convert_to_uint64,
)

if TYPE_CHECKING:
    MmsValuePointer = ctypes._Pointer[_sMmsValue]  # type: ignore
else:
    MmsValuePointer = ctypes.POINTER(_sMmsValue)


class MmsValueException(Exception): ...


class MmsType(Enum):
    """Enum to represent the type of a ``MmsValue``"""

    ARRAY = 0
    "array type (multiple elements of the same type)"

    STRUCTURE = 1
    "structure type (multiple elements of different types)"

    BOOLEAN = 2
    "boolean"

    BIT_STRING = 3
    "bit string"

    INTEGER = 4
    "signed integer"

    UNSIGNED = 5
    "unsigned integer"

    FLOAT = 6
    "floating point value (32 or 64 bit)"

    OCTET_STRING = 7
    "octet string"

    VISIBLE_STRING = 8
    "visible string - ANSI string"

    GENERALIZED_TIME = 9
    "Generalized time"

    BINARY_TIME = 10
    "Binary time"

    BCD = 11
    "Binary coded decimal (BCD) - not used"

    OBJ_ID = 12
    "object ID - not used"

    STRING = 13
    "Unicode string"

    UTC_TIME = 14
    "UTC time"

    DATA_ACCESS_ERROR = 15
    "Will be returned in case of an error (contains error code)"


class MmsVariableSpecification:
    def __init__(
        self,
        handle,
        responsableForDeletion: bool = False,
        parent: "MmsVariableSpecification | None" = None,
    ) -> None:
        self._handle = handle
        self._responsableForDeletion = responsableForDeletion
        self._parent = parent

    def __del__(self):
        if self._responsableForDeletion:
            Wrapper.lib.MmsVariableSpecification_destroy(self._handle)

    @property
    def handle(self):
        return self._handle

    def GetChildByName(self, name: str | bytes) -> "MmsVariableSpecification | None":
        name = convert_to_bytes(name)
        name = name.replace(b".", b"$")

        handle = Wrapper.lib.MmsVariableSpecification_getNamedVariableRecursive(self._handle, name)
        if handle:
            return MmsVariableSpecification(handle, parent=self)

        return None

    def GetType(self) -> MmsType:
        return MmsType(Wrapper.lib.MmsVariableSpecification_getType(self._handle))


class MmsDataAccessError(Enum):
    NO_RESPONSE = -2
    SUCCESS = -1
    OBJECT_INVALIDATED = 0
    HARDWARE_FAULT = 1
    TEMPORARILY_UNAVAILABLE = 2
    OBJECT_ACCESS_DENIED = 3
    OBJECT_UNDEFINED = 4
    INVALID_ADDRESS = 5
    TYPE_UNSUPPORTED = 6
    TYPE_INCONSISTENT = 7
    OBJECT_ATTRIBUTE_INCONSISTENT = 8
    OBJECT_ACCESS_UNSUPPORTED = 9
    OBJECT_NONE_EXISTENT = 10
    OBJECT_VALUE_INVALID = 11
    UNKNOWN = 12


class MmsValue:
    def __init__(self, handle: MmsValuePointer, responsable_for_deletion: bool = False) -> None:
        self._handle = handle
        self._responsable_for_deletion = responsable_for_deletion

    def __del__(self):
        if self._handle and self._responsable_for_deletion:
            Wrapper.lib.MmsValue_delete(self._handle)
            self._handle = 0

    @property
    def handle(self):
        """Pointer to the underlying C structure"""
        return self._handle

    def get_value(self):
        mms_type = self.get_type()

        if mms_type == MmsType.ARRAY:
            return [
                el if not isinstance(el := self.get_element(i), MmsValue) else el.get_value()
                for i in range(self.size())
            ]

        if mms_type == MmsType.STRUCTURE:
            return [
                el if not isinstance(el := self.get_element(i), MmsValue) else el.get_value()
                for i in range(self.size())
            ]

        if mms_type == MmsType.BOOLEAN:
            return self.to_bool()

        if mms_type == MmsType.BIT_STRING:
            return self.to_bitstring()

        if mms_type == MmsType.INTEGER:
            return self.to_int64()

        if mms_type == MmsType.UNSIGNED:
            return self.to_uint32()

        if mms_type == MmsType.FLOAT:
            return self.to_double()

        if mms_type == MmsType.OCTET_STRING:
            return self.to_octet_string()

        if mms_type == MmsType.VISIBLE_STRING:
            return self.to_string()

        if mms_type == MmsType.GENERALIZED_TIME:
            ...

        if mms_type == MmsType.BINARY_TIME:
            ...

        if mms_type == MmsType.BCD:
            ...

        if mms_type == MmsType.OBJ_ID:
            ...

        if mms_type == MmsType.STRING:
            return self.to_string()

        if mms_type == MmsType.UTC_TIME:
            return self.to_utc_time()

        if mms_type == MmsType.DATA_ACCESS_ERROR:
            return self.to_data_access_error()

    @staticmethod
    def new_bool(value: bool) -> "MmsValue":
        """Create a new MmsValue representing a boolean

        Parameters
        ----------
        value : bool
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newBoolean(value)
        return MmsValue(handle)

    def to_bool(self) -> bool:
        """Convert the MmsValue to a boolean"""
        return Wrapper.lib.MmsValue_getBoolean(self._handle)

    def set_bool(self, value: bool):
        Wrapper.lib.MmsValue_setBoolean(self._handle, value)

    @staticmethod
    def new_float(value: float) -> "MmsValue":
        """Create a new MmsValue representing a float

        Parameters
        ----------
        value : float
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newFloat(value)
        return MmsValue(handle)

    def to_float(self) -> float:
        """Convert the MmsValue to a float"""
        return Wrapper.lib.MmsValue_toFloat(self._handle)

    def set_float(self, value: float):
        Wrapper.lib.MmsValue_setFloat(self._handle, value)

    @staticmethod
    def new_double(value: float) -> "MmsValue":
        """Create a new MmsValue representing a double

        Parameters
        ----------
        value : float
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newDouble(value)
        return MmsValue(handle)

    def to_double(self) -> float:
        """Convert the MmsValue to a double"""
        return Wrapper.lib.MmsValue_toDouble(self._handle)

    def set_double(self, value: float):
        Wrapper.lib.MmsValue_setDouble(self._handle, value)

    @staticmethod
    def new_int8(value: int) -> "MmsValue":
        """Create a new MmsValue representing an int8

        Parameters
        ----------
        value : int
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newIntegerFromInt8(value)
        return MmsValue(handle)

    def set_int8(self, value: int):
        Wrapper.lib.MmsValue_setInt8(self._handle, value)

    @staticmethod
    def new_int16(value: int) -> "MmsValue":
        """Create a new MmsValue representing an int16

        Parameters
        ----------
        value : int
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newIntegerFromInt16(value)
        return MmsValue(handle)

    def set_int16(self, value: int):
        Wrapper.lib.MmsValue_setInt16(self._handle, value)

    @staticmethod
    def new_int32(value: int) -> "MmsValue":
        """Create a new MmsValue representing an int32

        Parameters
        ----------
        value : int
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newIntegerFromInt32(value)
        return MmsValue(handle)

    def to_int32(self) -> int:
        """Convert the MmsValue to an int32"""
        return Wrapper.lib.MmsValue_toInt32(self._handle)

    def set_int32(self, value: int):
        Wrapper.lib.MmsValue_setInt32(self._handle, value)

    @staticmethod
    def new_int64(value: int) -> "MmsValue":
        """Create a new MmsValue representing an int64

        Parameters
        ----------
        value : int
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newIntegerFromInt64(value)
        return MmsValue(handle)

    def to_int64(self) -> int:
        """Convert the MmsValue to an int64"""
        return Wrapper.lib.MmsValue_toInt64(self._handle)

    def set_int64(self, value: int):
        Wrapper.lib.MmsValue_setInt64(self._handle, value)

    def set_uint8(self, value: int):
        Wrapper.lib.MmsValue_setUint8(self._handle, value)

    def set_uint16(self, value: int):
        Wrapper.lib.MmsValue_setUint16(self._handle, value)

    @staticmethod
    def new_uint32(value: int) -> "MmsValue":
        """Create a new MmsValue representing an uint32

        Parameters
        ----------
        value : int
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newUnsignedFromUint32(value)
        return MmsValue(handle)

    def to_uint32(self) -> int:
        """Convert the MmsValue to an uint32"""
        return Wrapper.lib.MmsValue_toUint32(self._handle)

    def set_uint32(self, value: int):
        Wrapper.lib.MmsValue_setUint32(self._handle, value)

    @staticmethod
    def new_visible_string(value: str | bytes) -> "MmsValue":
        """Create a new MmsValue representing a visible string

        Parameters
        ----------
        value : str | bytes
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        value = convert_to_bytes(value)
        handle = Wrapper.lib.MmsValue_newVisibleString(value)
        return MmsValue(handle)

    def to_string(self) -> bytes:
        """Convert the MmsValue to a string"""
        return Wrapper.lib.MmsValue_toString(self._handle)

    @staticmethod
    def new_bitstring(value: int) -> "MmsValue":
        """Create a new MmsValue representing a bitstring

        Parameters
        ----------
        value : int
            Initial value

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newBitString(value)
        return MmsValue(handle)

    def to_bitstring(self) -> int:
        """Convert the MmsValue to a bitstring"""
        return Wrapper.lib.MmsValue_getBitStringAsInteger(self._handle)

    @staticmethod
    def new_octetstring(maxsize: int, size: int) -> "MmsValue":
        """Create a new MmsValue representing an empty octet string

        Parameters
        ----------
        maxsize : int
            _description_
        size : int
            _description_

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newOctetString(maxsize, size)
        return MmsValue(handle)

    def to_octet_string(self) -> bytearray:
        """Convert the MmsValue to a bytearray"""
        size = Wrapper.lib.MmsValue_getOctetStringSize(self._handle)
        buffer_ptr = Wrapper.lib.MmsValue_getOctetStringBuffer(self._handle)
        buffer = bytearray()
        data = ctypes.string_at(buffer_ptr, size)
        buffer.extend(data)
        return buffer

    @staticmethod
    def new_array(element_type: MmsVariableSpecification, size: int) -> "MmsValue":
        """Create a new MmsValue representing a array

        Parameters
        ----------
        element_type : MmsVariableSpecification
            _description_
        size : int
            _description_

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_createArray(element_type.handle, size)
        return MmsValue(handle)

    @staticmethod
    def new_empty_array(size: int) -> "MmsValue":
        """Create a new MmsValue representing an empty array

        Parameters
        ----------
        size : int
            _description_

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_createEmptyArray(size)
        return MmsValue(handle)

    @staticmethod
    def new_empty_structure(size: int) -> "MmsValue":
        """Create a new MmsValue representing an empty structure

        Parameters
        ----------
        size : int
            _description_

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_createEmptyStructure(size)
        return MmsValue(handle)

    @staticmethod
    def new_binary_time(large_format: bool) -> "MmsValue":
        """Create a new MmsValue representing a binary time

        Parameters
        ----------
        large_format : bool
            _description_

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newBinaryTime(large_format)
        return MmsValue(handle)

    @staticmethod
    def new_utc_time(
        timeval: datetime.datetime = datetime.datetime.now().astimezone(),
    ) -> "MmsValue":
        """Create a new MmsValue instance of type MMS_UTCTIME.

        Parameters
        ----------
        timeval : datetime.datetime, optional
            Time value, by default datetime.datetime.now().astimezone()

        Returns
        -------
        MmsValue
            _description_
        """
        val_uint64 = convert_to_uint64(timeval)
        return MmsValue.new_utc_time_ms(val_uint64)

    def to_utc_time_ms(self) -> int:
        """Convert the utc time in ms since epoch"""
        if self.get_type() == MmsType.UTC_TIME:
            return Wrapper.lib.MmsValue_getUtcTimeInMs(self._handle)
        raise MmsValueException("MmsType is not UTC_TIME")

    def to_utc_time(self) -> datetime.datetime:
        """Convert the MmsValue to a datetime"""
        ms = self.to_utc_time_ms()
        return convert_to_datetime(ms)

    @staticmethod
    def new_utc_time_s(timeval: int) -> "MmsValue":
        """Create a new MmsValue instance of type MMS_UTCTIME.

        Parameters
        ----------
        timeval : int
            time value as UNIX timestamp (seconds since epoch)

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newUtcTime(timeval)
        return MmsValue(handle)

    @staticmethod
    def new_utc_time_ms(timeval: int) -> "MmsValue":
        """Create a new MmsValue instance of type MMS_UTCTIME.

        Parameters
        ----------
        timeval : int
            time value as millisecond timestamp (milliseconds since epoch)

        Returns
        -------
        MmsValue
            _description_
        """
        handle = Wrapper.lib.MmsValue_newUtcTimeByMsTime(timeval)
        return MmsValue(handle)

    def get_type(self) -> MmsType:
        """Return the type of the MmsValue"""
        val = Wrapper.lib.MmsValue_getType(self._handle)
        return MmsType(val)

    def size(self) -> int:
        """Size of the MmsValue"""
        mms_type = self.get_type()
        if (mms_type == MmsType.ARRAY) or (mms_type == MmsType.STRUCTURE):
            return Wrapper.lib.MmsValue_getArraySize(self._handle)
        if mms_type == MmsType.BIT_STRING:
            return Wrapper.lib.MmsValue_getBitStringSize(self._handle)
        if mms_type == MmsType.OCTET_STRING:
            return Wrapper.lib.MmsValue_getOctetStringSize(self._handle)
        raise MmsValueException(
            f"{mms_type} is not supported, only ARRAY, STRUCTURE, "
            "BIT_STRING and OCTET_STRING type are supported"
        )

    def get_element(self, index: int) -> "MmsValue | None":
        mms_type = self.get_type()
        if mms_type in (MmsType.ARRAY, MmsType.STRUCTURE):
            if 0 <= index < self.size():
                value = Wrapper.lib.MmsValue_getElement(self._handle, index)
                if not value:
                    return None
                return MmsValue(value)
            raise IndexError("Index out of bounds")
        raise MmsValueException(
            f"{mms_type} is not supported, only ARRAY and STRUCTURE type are supported"
        )

    def __str__(self) -> str:
        return str(self.get_value())

    def to_data_access_error(self) -> MmsDataAccessError:
        """Convert the MmsValue to a MmsDataAccessError"""
        mms_type = self.get_type()
        if mms_type == MmsType.DATA_ACCESS_ERROR:
            value = Wrapper.lib.MmsValue_getDataAccessError(self._handle)
            return MmsDataAccessError(value)

        raise MmsValueException(
            f"{mms_type} is not supported, only DATA_ACCESS_ERROR type is supported"
        )
