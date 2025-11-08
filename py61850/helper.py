import ctypes
from datetime import datetime, timedelta, timezone


def address_of(obj: ctypes._Pointer | ctypes.c_void_p | int) -> int:
    if isinstance(obj, ctypes._Pointer):
        return ctypes.addressof(obj.contents)
    if isinstance(obj, ctypes._Pointer):
        return obj.value
    return obj


def convert_to_bytes(content: str | bytes) -> bytes:
    """Convert a string to a bytes

    Parameters
    ----------
    content : str | bytes
        _description_

    Returns
    -------
    bytes
        _description_
    """
    if isinstance(content, str):
        return content.encode("utf-8")
    return content


def convert_to_str(content: str | bytes) -> str:
    """_summary_

    Parameters
    ----------
    content : str | bytes
        _description_

    Returns
    -------
    str
        _description_
    """
    if isinstance(content, bytes):
        return content.decode("utf-8")
    return content


def convert_to_datetime(ms: float | int):
    timestamp = datetime(1970, 1, 1, 0, 0, 0, 0)
    timestamp = timestamp + timedelta(milliseconds=ms)
    return timestamp


def convert_to_uint64(timestamp: datetime) -> int:
    difference = timestamp - datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    return (
        difference.days * 86400000
        + difference.seconds * 1000
        + int(difference.microseconds / 1000)
    )
