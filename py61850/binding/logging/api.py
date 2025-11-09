"""Module for C binding with logging/logging_api.h"""

from ctypes import (
    CDLL,
    CFUNCTYPE,
    POINTER,
    Structure,
    c_bool,
    c_char_p,
    c_int,
    c_uint8,
    c_uint64,
    c_void_p,
)


class sLogStorage(Structure): ...


LogStorage = POINTER(sLogStorage)

LogEntryCallback = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter
    c_uint64,  # uint64_t timestamp
    c_uint64,  # uint64_t entryID
    c_bool,  # bool moreFollow
)

LogEntryDataCallback = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter
    c_char_p,  # const char* dataRef
    POINTER(c_uint8),  # uint8_t* data
    c_int,  # int dataSize
    c_uint8,  # uint8_t reasonCode
    c_bool,  # bool moreFollow
)


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    lib.LogStorage_setMaxLogEntries.argtypes = [
        LogStorage,  # LogStorage self
        c_int,  # int maxEntries
    ]
    lib.LogStorage_setMaxLogEntries.restype = None

    lib.LogStorage_getMaxLogEntries.argtypes = [
        LogStorage,  # LogStorage self
    ]
    lib.LogStorage_getMaxLogEntries.restype = c_int

    lib.LogStorage_addEntry.argtypes = [
        LogStorage,  # LogStorage self
        c_uint64,  # uint64_t timestamp
    ]
    lib.LogStorage_addEntry.restype = c_uint64

    lib.LogStorage_addEntryData.argtypes = [
        LogStorage,  # LogStorage self
        c_uint64,  # uint64_t entryID
        c_char_p,  # const char* dataRef
        POINTER(c_uint8),  # uint8_t* data
        c_int,  # int dataSize
        c_uint8,  # uint8_t reasonCode
    ]
    lib.LogStorage_addEntryData.restype = c_bool

    lib.LogStorage_getEntries.argtypes = [
        LogStorage,  # LogStorage self
        c_uint64,  # uint64_t startingTime
        c_uint64,  # uint64_t endingTime
        LogEntryCallback,  # LogEntryCallback entryCallback
        LogEntryDataCallback,  # LogEntryDataCallback entryDataCallback
        c_void_p,  # void* parameter
    ]
    lib.LogStorage_getEntries.restype = c_bool

    lib.LogStorage_getEntriesAfter.argtypes = [
        LogStorage,  # LogStorage self
        c_uint64,  # uint64_t startingTime
        c_uint64,  # uint64_t entryID
        LogEntryCallback,  # LogEntryCallback entryCallback
        LogEntryDataCallback,  # LogEntryDataCallback entryDataCallback
        c_void_p,  # void* parameter
    ]
    lib.LogStorage_getEntriesAfter.restype = c_bool

    lib.LogStorage_getOldestAndNewestEntries.argtypes = [
        LogStorage,  # LogStorage self
        POINTER(c_uint64),  # uint64_t* newEntry
        POINTER(c_uint64),  # uint64_t* newEntryTime
        POINTER(c_uint64),  # uint64_t* oldEntry
        POINTER(c_uint64),  # uint64_t* oldEntryTime
    ]
    lib.LogStorage_getOldestAndNewestEntries.restype = c_bool

    lib.LogStorage_destroy.argtypes = [
        LogStorage,  # LogStorage self
    ]
    lib.LogStorage_destroy.restype = None

    sqlite_enabled = getattr(lib, "SqliteLogStorage_createInstance", None) is not None
    if sqlite_enabled:
        lib.SqliteLogStorage_createInstance.argtypes = [
            c_char_p,  # const char* filename
        ]
        lib.SqliteLogStorage_createInstance.restype = LogStorage
