"""Implements function and class relative to dataset on client side"""

from ctypes import c_void_p
from typing import TYPE_CHECKING

from ..binding.loader import Wrapper
from ..common import MmsValue

if TYPE_CHECKING:
    from .connection import IedConnection


class DataSet:
    """Representation of a dataset on client side"""

    def __init__(self, handle: c_void_p, ied_connection: "IedConnection") -> None:
        self._handle = handle
        self._values = None
        self._ied_connection = ied_connection

    def __del__(self):
        Wrapper.lib.ClientDataSet_destroy(self._handle)

    @property
    def handle(self):
        """Pointer to the underlying C structure"""
        return self._handle

    @property
    def reference(self) -> bytes:
        """Object reference of the data set."""

        value = Wrapper.lib.ClientDataSet_getReference(self._handle)
        return value

    @property
    def values(self) -> MmsValue:
        """Return data set values locally stored in the instance.

        See Also
        --------
        update_dataset_values
        """
        handle = Wrapper.lib.ClientDataSet_getValues(self._handle)
        self._values = MmsValue(handle, False)
        return self._values

    @property
    def size(self) -> int:
        """Number of member of the data set"""
        return Wrapper.lib.ClientDataSet_getDataSetSize(self._handle)

    def update_values(self):
        """Update the values stored in the dataset"""
        self._ied_connection.update_dataset_values(self)
