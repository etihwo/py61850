"""Module for C binding with iec61850/inc/iec61850_config_file_parser.h"""

from ctypes import CDLL, POINTER, c_char_p, c_void_p

from .model import IedModel

FileHandle = c_void_p


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    lib.ConfigFileParser_createModelFromConfigFileEx.argtypes = [
        c_char_p,  # const char* filename
    ]
    lib.ConfigFileParser_createModelFromConfigFileEx.restype = POINTER(IedModel)

    lib.ConfigFileParser_createModelFromConfigFile.argtypes = [
        FileHandle,  # FileHandle fileHandle
    ]
    lib.ConfigFileParser_createModelFromConfigFile.restype = POINTER(IedModel)
