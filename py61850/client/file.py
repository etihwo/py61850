"""Implements function and class relative to file on client side"""

import datetime
from ctypes import c_void_p
from typing import TYPE_CHECKING

from ..binding.loader import Wrapper
from ..helper import convert_to_datetime

if TYPE_CHECKING:
    from .connection import IedConnection


class FileDirectoryEntry:
    """File directory entry"""

    def __init__(self, handle: c_void_p, ied_connection: "IedConnection") -> None:
        self._handle = handle
        self._ied_connection = ied_connection

    def __del__(self):
        Wrapper.lib.FileDirectoryEntry_destroy(self._handle)

    @property
    def filename(self) -> bytes:
        """Name of the file."""
        return Wrapper.lib.FileDirectoryEntry_getFileName(self._handle)

    @property
    def file_size(self) -> int:
        """File size in bytes."""
        return Wrapper.lib.FileDirectoryEntry_getFileSize(self._handle)

    @property
    def last_modified(self) -> datetime.datetime:
        """Timestamp of last modification of the file."""
        ms = Wrapper.lib.FileDirectoryEntry_getLastModified(self._handle)
        return convert_to_datetime(ms)

    def download(self) -> tuple[int, bytearray]:
        """Download the file

        Returns
        -------
        tuple[int, bytearray]
            Return byte received and content of the file
        """
        return self._ied_connection.download_file(self.filename)
