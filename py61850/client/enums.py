"""Implement Enum for client side module"""

from enum import Enum


class IedClientError(Enum):
    """Used to describe the error reason for most client side service functions"""

    # general errors
    OK = 0
    """No error occurred - service request has been successful"""

    NOT_CONNECTED = 1
    """The service request can not be executed because the client is not
    yet connected"""

    ALREADY_CONNECTED = 2
    """Connect service not execute because the client is already connected"""

    CONNECTION_LOST = 3
    """The service request can not be executed caused by a loss of
    connection"""

    SERVICE_NOT_SUPPORTED = 4
    """The service or some given parameters are not supported by the
    client stack or by the server"""

    CONNECTION_REJECTED = 5
    """Connection rejected by server"""

    OUTSTANDING_CALL_LIMIT_REACHED = 6
    """Cannot send request because outstanding call limit is reached"""

    # client side errors

    USER_PROVIDED_INVALID_ARGUMENT = 10
    """API function has been called with an invalid argument"""

    ENABLE_REPORT_FAILED_DATASET_MISMATCH = 11

    OBJECT_REFERENCE_INVALID = 12
    """The object provided object reference is invalid (there is a
    syntactical error)."""

    UNEXPECTED_VALUE_RECEIVED = 13
    """Received object is of unexpected type"""

    # service error - error reported by server
    TIMEOUT = 20
    """The communication to the server failed with a timeout"""

    ACCESS_DENIED = 21
    """The server rejected the access to the requested object/service due
    to access control"""

    OBJECT_DOES_NOT_EXIST = 22
    """The server reported that the requested object does not exist
    (returned by server)"""

    OBJECT_EXISTS = 23
    """The server reported that the requested object already exists"""

    OBJECT_ACCESS_UNSUPPORTED = 24
    """The server does not support the requested access method (returned
    by server)"""

    TYPE_INCONSISTENT = 25
    """The server expected an object of another type (returned by server)"""

    TEMPORARILY_UNAVAILABLE = 26
    """The object or service is temporarily unavailable (returned by
    server)"""

    OBJECT_UNDEFINED = 27
    """The specified object is not defined in the server (returned by
    server)"""

    INVALID_ADDRESS = 28
    """The specified address is invalid (returned by server)"""

    HARDWARE_FAULT = 29
    """Service failed due to a hardware fault (returned by server)"""

    TYPE_UNSUPPORTED = 30
    """The requested data type is not supported by the server (returned by
    server)"""

    OBJECT_ATTRIBUTE_INCONSISTENT = 31
    """The provided attributes are inconsistent (returned by server)"""

    OBJECT_VALUE_INVALID = 32
    """The provided object value is invalid (returned by server)"""

    OBJECT_INVALIDATED = 33
    """The object is invalidated (returned by server)"""

    MALFORMED_MESSAGE = 34
    """Received an invalid response message from the server"""

    OBJECT_CONSTRAINT_CONFLICT = 35
    """Service was not executed because required resource is still in use"""

    SERVICE_NOT_IMPLEMENTED = 98
    """Service not implemented"""

    UNKNOWN = 99
    """unknown error"""


class IedConnectionState(Enum):
    """Connection state of the IedConnection instance - either
    closed(idle), connecting, connected, or closing)"""

    CLOSED = 0
    CONNECTING = 1
    CONNECTED = 2
    CLOSING = 3


class AcseAuthenticationMechanism(Enum):
    """Authentication mechanism used by AcseAuthenticator"""

    NONE = 0
    """Neither ACSE nor TLS authentication used"""
    PASSWORD = 1
    """Use ACSE password for client authentication"""
    CERTIFICATE = 2
    """Use ACSE certificate for client authentication"""
    TLS = 4
    """Use TLS certificate for client authentication"""
