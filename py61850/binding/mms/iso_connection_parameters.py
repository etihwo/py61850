"""Module for C binding with mms/inc/iso_connection_parameters.h"""

from ctypes import CFUNCTYPE, POINTER, Structure, c_bool, c_void_p

AcseAuthenticationParameter = c_void_p


class IsoApplicationReference(Structure): ...


AcseAuthenticator = CFUNCTYPE(
    c_bool,  # return type: bool
    c_void_p,  # void* parameter
    AcseAuthenticationParameter,  # AcseAuthenticationParameter authParameter,
    POINTER(c_void_p),  #  void** securityToken,
    POINTER(IsoApplicationReference),  # IsoApplicationReference* appReference
)
