"""Module for C binding with mms/inc/mms_value.h"""

from ctypes import (
    CDLL,
    POINTER,
    Structure,
    c_bool,
    c_char_p,
    c_double,
    c_float,
    c_int,
    c_int8,
    c_int16,
    c_int32,
    c_int64,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
)


class sMmsValue(Structure): ...


class sMmsVariableSpecification(Structure): ...


MmsVariableSpecification = sMmsVariableSpecification
MmsValue = sMmsValue
MmsType = c_int
MmsDataAccessError = c_int


def setup_prototypes(lib: CDLL):
    ####################################################
    # Array functions
    ####################################################
    lib.MmsValue_createArray.argtypes = [
        POINTER(MmsVariableSpecification),  # const MmsVariableSpecification* elementType
        c_int,  #  int size
    ]
    lib.MmsValue_createArray.restype = POINTER(MmsValue)

    lib.MmsValue_getArraySize.argtypes = [
        POINTER(MmsValue),  # const MmsValue* array
    ]
    lib.MmsValue_getArraySize.restype = c_uint32

    lib.MmsValue_getElement.argtypes = [
        POINTER(MmsValue),  # const MmsValue* array
        c_int,  #  index
    ]
    lib.MmsValue_getElement.restype = POINTER(MmsValue)

    lib.MmsValue_createEmptyArray.argtypes = [
        c_int,  # int size
    ]
    lib.MmsValue_createEmptyArray.restype = POINTER(MmsValue)

    lib.MmsValue_setElement.argtypes = [
        POINTER(MmsValue),  # MmsValue* complexValue
        c_int,  # int index
        POINTER(MmsValue),  # MmsValue* elementValue
    ]
    lib.MmsValue_setElement.restype = None

    ####################################################
    #  Basic type functions
    ####################################################

    lib.MmsValue_getDataAccessError.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_getDataAccessError.restype = MmsDataAccessError

    lib.MmsValue_toInt64.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_toInt64.restype = c_int64

    lib.MmsValue_toInt32.argtypes = [
        POINTER(MmsValue),  # const MmsValue* value
    ]
    lib.MmsValue_toInt32.restype = c_int32

    lib.MmsValue_toUint32.argtypes = [
        POINTER(MmsValue),  # const MmsValue* value
    ]
    lib.MmsValue_toUint32.restype = c_uint32

    lib.MmsValue_toDouble.argtypes = [
        POINTER(MmsValue),  # const MmsValue* value
    ]
    lib.MmsValue_toDouble.restype = c_double

    lib.MmsValue_toFloat.argtypes = [
        POINTER(MmsValue),  # const MmsValue* value
    ]
    lib.MmsValue_toFloat.restype = c_float

    lib.MmsValue_toUnixTimestamp.argtypes = [
        POINTER(MmsValue),  # const MmsValue* value
    ]
    lib.MmsValue_toUnixTimestamp.restype = c_uint32

    lib.MmsValue_setFloat.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_float,  # float newFloatValue
    ]
    lib.MmsValue_setFloat.restype = None

    lib.MmsValue_setDouble.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_double,  # double newFloatValue
    ]
    lib.MmsValue_setDouble.restype = None

    lib.MmsValue_setInt8.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_int8,  # int8_t integer
    ]
    lib.MmsValue_setInt8.restype = None

    lib.MmsValue_setInt16.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_int16,  # int16_t integer
    ]
    lib.MmsValue_setInt16.restype = None

    lib.MmsValue_setInt32.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_int32,  # int32_t integer
    ]
    lib.MmsValue_setInt32.restype = None

    lib.MmsValue_setInt64.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_int64,  # int64_t integer
    ]
    lib.MmsValue_setInt64.restype = None

    lib.MmsValue_setUint8.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_uint8,  # uint8_t integer
    ]
    lib.MmsValue_setUint8.restype = None

    lib.MmsValue_setUint16.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_uint16,  # uint16_t integer
    ]
    lib.MmsValue_setUint16.restype = None

    lib.MmsValue_setUint32.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_uint32,  # uint32_t integer
    ]
    lib.MmsValue_setUint32.restype = None

    lib.MmsValue_setBoolean.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_bool,  # bool boolValue
    ]
    lib.MmsValue_setBoolean.restype = None

    lib.MmsValue_getBoolean.argtypes = [
        POINTER(MmsValue),  # const MmsValue* value
    ]
    lib.MmsValue_getBoolean.restype = bool

    lib.MmsValue_toString.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_toString.restype = c_char_p

    lib.MmsValue_getStringSize.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
    ]
    lib.MmsValue_getStringSize.restype = c_int

    lib.MmsValue_setVisibleString.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_char_p,  # const char* string
    ]
    lib.MmsValue_setVisibleString.restype = None

    lib.MmsValue_setBitStringBit.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_int,  # int bitPos
        c_bool,  # bool value
    ]
    lib.MmsValue_setBitStringBit.restype = None

    lib.MmsValue_getBitStringBit.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
        c_int,  # int bitPos
    ]
    lib.MmsValue_getBitStringBit.restype = c_bool

    lib.MmsValue_deleteAllBitStringBits.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_deleteAllBitStringBits.restype = None

    lib.MmsValue_getBitStringSize.argtypes = [
        POINTER(MmsValue),  # const MmsValue* array
    ]
    lib.MmsValue_getBitStringSize.restype = c_int

    lib.MmsValue_getBitStringByteSize.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_getBitStringByteSize.restype = c_int

    lib.MmsValue_getNumberOfSetBits.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_getNumberOfSetBits.restype = c_int

    lib.MmsValue_setAllBitStringBits.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
    ]
    lib.MmsValue_setAllBitStringBits.restype = None

    lib.MmsValue_getBitStringAsInteger.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_getBitStringAsInteger.restype = c_uint32

    lib.MmsValue_setBitStringFromInteger.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_uint32,  # uint32_t intValue
    ]
    lib.MmsValue_setBitStringFromInteger.restype = None

    lib.MmsValue_getBitStringAsIntegerBigEndian.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_getBitStringAsIntegerBigEndian.restype = c_uint32

    lib.MmsValue_setBitStringFromIntegerBigEndian.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_uint32,  # uint32_t intValue
    ]
    lib.MmsValue_setBitStringFromIntegerBigEndian.restype = None

    lib.MmsValue_setUtcTime.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_uint32,  # uint32_t timeval
    ]
    lib.MmsValue_setUtcTime.restype = POINTER(MmsValue)

    lib.MmsValue_setUtcTimeMs.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_uint64,  # uint64_t timeval
    ]
    lib.MmsValue_setUtcTimeMs.restype = POINTER(MmsValue)

    lib.MmsValue_setUtcTimeByBuffer.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        POINTER(c_uint8),  # const uint8_t* buffer
    ]
    lib.MmsValue_setUtcTimeByBuffer.restype = None

    lib.MmsValue_getUtcTimeBuffer.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
    ]
    lib.MmsValue_getUtcTimeBuffer.restype = c_uint8

    lib.MmsValue_getUtcTimeInMs.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
    ]
    lib.MmsValue_getUtcTimeInMs.restype = c_uint64

    # /**
    #  * \brief Get a millisecond time value and optional us part from an MmsValue object of MMS_UTCTIME type.
    #  *
    #  * \param self MmsValue instance to operate on. Has to be of a type MMS_UTCTIME.
    #  * \param usec a pointer to store the us (microsecond) value.
    #  *
    #  * \return the value in milliseconds since epoch (1970/01/01 00:00 UTC)
    #  */
    # LIB61850_API uint64_t
    # MmsValue_getUtcTimeInMsWithUs(const MmsValue* self, uint32_t* usec);

    # /**
    #  * \brief set the TimeQuality byte of the UtcTime
    #  *
    #  * Meaning of the bits in the timeQuality byte:
    #  *
    #  * bit 7 = leapSecondsKnown
    #  * bit 6 = clockFailure
    #  * bit 5 = clockNotSynchronized
    #  * bit 0-4 = subsecond time accuracy (number of significant bits of subsecond time)
    #  *
    #  * \param self MmsValue instance to operate on. Has to be of a type MMS_UTCTIME.
    #  * \param timeQuality the byte representing the time quality
    #  */
    # LIB61850_API void
    # MmsValue_setUtcTimeQuality(MmsValue* self, uint8_t timeQuality);

    # /**
    #  * \brief Update an MmsValue object of type MMS_UTCTIME with a millisecond time.
    #  *
    #  * Meaning of the bits in the timeQuality byte:
    #  *
    #  * bit 7 = leapSecondsKnown
    #  * bit 6 = clockFailure
    #  * bit 5 = clockNotSynchronized
    #  * bit 0-4 = subsecond time accuracy (number of significant bits of subsecond time)
    #  *
    #  * \param self MmsValue instance to operate on. Has to be of a type MMS_UTCTIME.
    #  * \param timeval the new value in milliseconds since epoch (1970/01/01 00:00 UTC)
    #  * \param timeQuality the byte representing the time quality
    #  *
    #  * \return the updated MmsValue instance
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_setUtcTimeMsEx(MmsValue* self, uint64_t timeval, uint8_t timeQuality);

    lib.MmsValue_getUtcTimeQuality.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_getUtcTimeQuality.restype = c_uint8

    # /**
    #  * \brief Update an MmsValue object of type MMS_BINARYTIME with a millisecond time.
    #  *
    #  * \param self MmsValue instance to operate on. Has to be of a type MMS_UTCTIME.
    #  * \param timeval the new value in milliseconds since epoch (1970/01/01 00:00 UTC)
    #  */
    # LIB61850_API void
    # MmsValue_setBinaryTime(MmsValue* self, uint64_t timestamp);

    lib.MmsValue_getBinaryTimeAsUtcMs.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_getBinaryTimeAsUtcMs.restype = c_uint64

    # /**
    #  * \brief Set the value of an MmsValue object of type MMS_OCTET_STRING.
    #  *
    #  * This method will copy the provided buffer to the internal buffer of the
    #  * MmsValue instance. This will only happen if the internal buffer size is large
    #  * enough for the new value. Otherwise the object value is not changed.
    #  *
    #  * \param self MmsValue instance to operate on. Has to be of a type MMS_OCTET_STRING.
    #  * \param buf the buffer that contains the new value
    #  * \param size the size of the buffer that contains the new value
    #  */
    # LIB61850_API void
    # MmsValue_setOctetString(MmsValue* self, const uint8_t* buf, int size);

    # /**
    #  * \brief Set a single octet of an MmsValue object of type MMS_OCTET_STRING.
    #  *
    #  * This method will copy the provided octet to the internal buffer of the
    #  * MmsValue instance, at the 'octetPos' position. This will only happen
    #  * if the internal buffer size is large enough. Otherwise the object value is not changed.
    #  *
    #  * \param self MmsValue instance to operate on. Has to be of a type MMS_OCTET_STRING.
    #  * \param octetPos the position of the octet in the octet string. Starting with 0.
    #       The octet with position 0 is the first octet if the MmsValue instance is serialized.
    #  * \param value the new value of the octet (0 to 255, or 0x00 to 0xFF)
    #  */
    # LIB61850_API void
    # MmsValue_setOctetStringOctet(MmsValue* self, int octetPos, uint8_t value);

    lib.MmsValue_getOctetStringSize.argtypes = [
        POINTER(MmsValue),  # const MmsValue* array
    ]
    lib.MmsValue_getOctetStringSize.restype = c_uint16

    lib.MmsValue_getOctetStringMaxSize.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
    ]
    lib.MmsValue_getOctetStringMaxSize.restype = c_uint16

    lib.MmsValue_getOctetStringBuffer.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
    ]
    lib.MmsValue_getOctetStringBuffer.restype = POINTER(c_uint8)

    lib.MmsValue_getOctetStringOctet.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        c_int,  # int octetPos
    ]
    lib.MmsValue_getOctetStringOctet.restype = c_uint8

    lib.MmsValue_update.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
        POINTER(MmsValue),  # onst MmsValue* source
    ]
    lib.MmsValue_update.restype = c_bool

    lib.MmsValue_equals.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
        POINTER(MmsValue),  # const MmsValue* otherValue
    ]
    lib.MmsValue_equals.restype = c_bool

    lib.MmsValue_equalTypes.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
        POINTER(MmsValue),  # const MmsValue* otherValue
    ]
    lib.MmsValue_equalTypes.restype = c_bool

    ####################################################
    #  * Constructors and destructors
    ####################################################

    # LIB61850_API MmsValue*
    # MmsValue_newDataAccessError(MmsDataAccessError accessError);

    lib.MmsValue_newInteger.argtypes = [
        c_int,  # int size
    ]
    lib.MmsValue_newInteger.restype = POINTER(MmsValue)

    lib.MmsValue_newUnsigned.argtypes = [
        c_int,  # int size
    ]
    lib.MmsValue_newUnsigned.restype = POINTER(MmsValue)

    lib.MmsValue_newBoolean.argtypes = [
        c_bool,  # bool boolean
    ]
    lib.MmsValue_newBoolean.restype = POINTER(MmsValue)

    lib.MmsValue_newBitString.argtypes = [
        c_int,  # int bitSize
    ]
    lib.MmsValue_newBitString.restype = POINTER(MmsValue)

    lib.MmsValue_newOctetString.argtypes = [
        c_int,  # int bitSize
        c_int,  # int maxSize
    ]
    lib.MmsValue_newOctetString.restype = POINTER(MmsValue)

    # LIB61850_API MmsValue*
    # MmsValue_newStructure(const MmsVariableSpecification* typeSpec);

    lib.MmsValue_createEmptyStructure.argtypes = [
        c_int,  # int size
    ]
    lib.MmsValue_createEmptyStructure.restype = POINTER(MmsValue)

    # LIB61850_API MmsValue*
    # MmsValue_newDefaultValue(const MmsVariableSpecification* typeSpec);

    lib.MmsValue_newIntegerFromInt8.argtypes = [
        c_int8,  # int8_t integer
    ]
    lib.MmsValue_newIntegerFromInt8.restype = POINTER(MmsValue)

    lib.MmsValue_newIntegerFromInt16.argtypes = [
        c_int16,  # int16_t integer
    ]
    lib.MmsValue_newIntegerFromInt16.restype = POINTER(MmsValue)

    lib.MmsValue_newIntegerFromInt32.argtypes = [
        c_int32,  # int32_t integer
    ]
    lib.MmsValue_newIntegerFromInt32.restype = POINTER(MmsValue)

    lib.MmsValue_newIntegerFromInt64.argtypes = [
        c_int64,  # int64_t integer
    ]
    lib.MmsValue_newIntegerFromInt64.restype = POINTER(MmsValue)

    lib.MmsValue_newUnsignedFromUint32.argtypes = [
        c_uint32,  # uint32_t integer
    ]
    lib.MmsValue_newUnsignedFromUint32.restype = POINTER(MmsValue)

    lib.MmsValue_newFloat.argtypes = [
        c_float,  # float value
    ]
    lib.MmsValue_newFloat.restype = POINTER(MmsValue)

    lib.MmsValue_newDouble.argtypes = [
        c_double,  # double value
    ]
    lib.MmsValue_newDouble.restype = POINTER(MmsValue)

    lib.MmsValue_clone.argtypes = [
        POINTER(MmsValue),  # const MmsValue* self
    ]
    lib.MmsValue_clone.restype = POINTER(MmsValue)

    # /**
    #  * \brief Create a (deep) copy of an MmsValue instance in a user provided buffer
    #  *
    #  * This operation copies the give MmsValue instance to a user provided buffer.
    #  *
    #  * \param self the MmsValue instance that will be cloned
    #  * \param destinationAddress the start address of the user provided buffer
    #  *
    #  * \return a pointer to the position in the buffer just after the last byte written.
    #  */
    # LIB61850_API uint8_t*
    # MmsValue_cloneToBuffer(const MmsValue* self, uint8_t* destinationAddress);

    # /**
    #  * \brief Determine the required amount of bytes by a clone.
    #  *
    #  * This function is intended to be used to determine the buffer size of a clone operation
    #  * (MmsValue_cloneToBuffer) in advance.
    #  *
    #  * \param self the MmsValue instance
    #  *
    #  * \return the number of bytes required by a clone
    #  */
    # LIB61850_API int
    # MmsValue_getSizeInMemory(const MmsValue* self);

    lib.MmsValue_delete.argtypes = [
        POINTER(MmsValue),  # MmsValue* self
    ]
    lib.MmsValue_delete.restype = None

    # /**
    #  * \brief Delete an MmsValue instance.
    #  *
    #  * This operation frees all dynamically allocated memory of the MmsValue instance.
    #  * If the instance is of type MMS_STRUCTURE or MMS_ARRAY all child elements will
    #  * be deleted too.
    #  *
    #  * NOTE: this functions only frees the instance if deleteValue field = 0!
    #  *
    #  *
    #  * \param self the MmsValue instance to be deleted.
    #  */
    # LIB61850_API void
    # MmsValue_deleteConditional(MmsValue* value);

    # /**
    #  * \brief Create a new MmsValue instance of type MMS_VISIBLE_STRING.
    #  *
    #  * This function will allocate as much memory as required to hold the string and sets the maximum size of
    #  * the string to this size.
    #  *
    #  * \param string a text string that should be the value of the new instance of NULL for an empty string.
    #  *
    #  * \return new MmsValue instance of type MMS_VISIBLE_STRING
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_newVisibleString(const char* string);

    # /**
    #  * \brief Create a new MmsValue instance of type MMS_VISIBLE_STRING.
    #  *
    #  * This function will create a new empty MmsValue string object. The maximum size of the string is set
    #  * according to the size parameter. The function allocates as much memory as is required to hold a string
    #  * of the maximum size.
    #  *
    #  * \param size the new maximum size of the string.
    #  *
    #  * \return new MmsValue instance of type MMS_VISIBLE_STRING
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_newVisibleStringWithSize(int size);

    lib.MmsValue_newMmsStringWithSize.argtypes = [
        c_int,  # int size
    ]
    lib.MmsValue_newMmsStringWithSize.restype = POINTER(MmsValue)

    lib.MmsValue_newBinaryTime.argtypes = [
        c_bool,  # bool timeOfDay
    ]
    lib.MmsValue_newBinaryTime.restype = POINTER(MmsValue)

    # /**
    #  * \brief Create a new MmsValue instance of type MMS_VISIBLE_STRING from the specified byte array
    #  *
    #  * \param byteArray the byte array containing the string data
    #  * \param size the size of the byte array
    #  *
    #  * \return new MmsValue instance of type MMS_VISIBLE_STRING
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_newVisibleStringFromByteArray(const uint8_t* byteArray, int size);

    # /**
    #  * \brief Create a new MmsValue instance of type MMS_STRING from the specified byte array
    #  *
    #  * \param byteArray the byte array containing the string data
    #  * \param size the size of the byte array
    #  *
    #  * \return new MmsValue instance of type MMS_STRING
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_newMmsStringFromByteArray(const uint8_t* byteArray, int size);

    # /**
    #  * \brief Create a new MmsValue instance of type MMS_STRING.
    #  *
    #  * \param string a text string that should be the value of the new instance of NULL for an empty string.
    #  *
    #  * \return new MmsValue instance of type MMS_STRING
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_newMmsString(const char* string);

    # /**
    #  * \brief Set the value of MmsValue instance of type MMS_STRING
    #  *
    #  * \param string a text string that will be the new value of the instance
    #  */
    # LIB61850_API void
    # MmsValue_setMmsString(MmsValue* value, const char* string);

    lib.MmsValue_newUtcTime.argtypes = [
        c_uint32,  # uint32_t timeval
    ]
    lib.MmsValue_newUtcTime.restype = POINTER(MmsValue)

    lib.MmsValue_newUtcTimeByMsTime.argtypes = [
        c_uint64,  # uint64_t timeval
    ]
    lib.MmsValue_newUtcTimeByMsTime.restype = POINTER(MmsValue)

    # LIB61850_API void
    # MmsValue_setDeletable(MmsValue* self);

    # LIB61850_API void
    # MmsValue_setDeletableRecursive(MmsValue* value);

    # /**
    #  * \brief Check if the MmsValue instance has the deletable flag set.
    #  *
    #  * The deletable flag indicates if an libiec61850 API client should call the
    #  * MmsValue_delete() method or not if the MmsValue instance was passed to the
    #  * client by an API call or callback method.
    #  *
    #  * \param self the MmsValue instance
    #  *
    #  * \return 1 if deletable flag is set, otherwise 0
    #  */
    # LIB61850_API int
    # MmsValue_isDeletable(MmsValue* self);

    # /**
    #  * \brief Get the MmsType of an MmsValue instance
    #  *
    #  * \param self the MmsValue instance
    #  */
    # LIB61850_API MmsType
    # MmsValue_getType(const MmsValue* self);

    lib.MmsValue_getType.argtypes = [
        POINTER(MmsValue),  # const MmsValue* array
    ]
    lib.MmsValue_getType.restype = MmsType

    # /**
    #  * \brief Get a sub-element of a MMS_STRUCTURE value specified by a path name.
    #  *
    #  * \param self the MmsValue instance
    #  * \param varSpec - type specification if the MMS_STRUCTURE value
    #  * \param mmsPath - path (in MMS variable name syntax) to specify the sub element.
    #  *
    #  * \return the sub elements MmsValue instance or NULL if the element does not exist
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_getSubElement(MmsValue* self, MmsVariableSpecification* varSpec, char* mmsPath);

    # /**
    #  * \brief return the value type as a human readable string
    #  *
    #  * \param self the MmsValue instance
    #  *
    #  * \return the value type as a human readable string
    #  */
    # LIB61850_API const char*
    # MmsValue_getTypeString(MmsValue* self);

    # /**
    #  * \brief create a string representation of the MmsValue object in the provided buffer
    #  *
    #  * NOTE: This function is for debugging purposes only. It may not be aimed to be used
    #  * in embedded systems. It requires a full featured snprintf function.
    #  *
    #  * \param self the MmsValue instance
    #  * \param buffer the buffer where to copy the string representation
    #  * \param bufferSize the size of the provided buffer
    #  *
    #  * \return a pointer to the start of the buffer
    #  */
    # LIB61850_API const char*
    # MmsValue_printToBuffer(const MmsValue* self, char* buffer, int bufferSize);

    # /**
    #  * \brief create a new MmsValue instance from a BER encoded MMS Data element (deserialize)
    #  *
    #  * WARNING: API changed with version 1.0.3 (added endBufPos parameter)
    #  *
    #  * \param buffer the buffer to read from
    #  * \param bufPos the start position of the mms value data in the buffer
    #  * \param bufferLength the length of the buffer
    #  * \param endBufPos the position in the buffer after the read MMS data element (NULL if not required)
    #  *
    #  * \return the MmsValue instance created from the buffer
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_decodeMmsData(uint8_t* buffer, int bufPos, int bufferLength, int* endBufPos);

    # /**
    #  * \brief create a new MmsValue instance from a BER encoded MMS Data element (deserialize) with a defined maximum recursion depth
    #  *
    #  * \param buffer the buffer to read from
    #  * \param bufPos the start position of the mms value data in the buffer
    #  * \param bufferLength the length of the buffer
    #  * \param endBufPos the position in the buffer after the read MMS data element (NULL if not required)
    #  * \param maxDepth the maximum recursion depth
    #  *
    #  * \return the MmsValue instance created from the buffer
    #  */
    # LIB61850_API MmsValue*
    # MmsValue_decodeMmsDataMaxRecursion(uint8_t* buffer, int bufPos, int bufferLength, int* endBufPos, int maxDepth);

    # /**
    #  * \brief Serialize the MmsValue instance as BER encoded MMS Data element
    #  *
    #  * \param self the MmsValue instance
    #  *
    #  * \param buffer the buffer to encode the MMS data element
    #  * \param bufPos the position in the buffer where to start encoding
    #  * \param encode encode to buffer (true) or calculate length only (false)
    #  *
    #  * \return the encoded length of the corresponding MMS data element
    #  */
    # LIB61850_API int
    # MmsValue_encodeMmsData(MmsValue* self, uint8_t* buffer, int bufPos, bool encode);

    # /**
    #  * \brief Get the maximum possible BER encoded size of the MMS data element
    #  *
    #  * \param self the MmsValue instance
    #  *
    #  * \return the maximum encoded size in bytes of the MMS data element
    #  */
    # LIB61850_API int
    # MmsValue_getMaxEncodedSize(MmsValue* self);

    # /**
    #  * \brief Calculate the maximum encoded size of a variable of this type
    #  *
    #  * \param self the MMS variable specification instance
    #  */
    # LIB61850_API int
    # MmsVariableSpecification_getMaxEncodedSize(MmsVariableSpecification* self);

    # /**
    #  * \brief Convert an MmsError to a string
    #  *
    #  * \param err the error to convert
    #  *
    #  * \return a static string representing the error
    #  */
    # LIB61850_API const char*
    # MmsError_toString(MmsError err);
