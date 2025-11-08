import ctypes
from typing import TYPE_CHECKING

from ..binding.common.linked_list import SLinkedList as _sLinkedList
from ..binding.loader import Wrapper
from ..helper import convert_to_bytes

if TYPE_CHECKING:
    LinkedListPointer = ctypes._Pointer[_sLinkedList]
else:
    LinkedListPointer = ctypes.POINTER(_sLinkedList)


class LinkedList:
    """LinkedList"""

    def __init__(self, handle: LinkedListPointer, responsable_for_deletion: bool = False) -> None:
        self._handle = handle
        self._responsable_for_deletion = responsable_for_deletion

    def __del__(self):
        if self._responsable_for_deletion and self._handle:
            Wrapper.lib.LinkedList_destroy(self._handle)

    @staticmethod
    def create_new() -> "LinkedList":
        """Create an empty LinkedList"""
        handle = Wrapper.lib.LinkedList_create()
        return LinkedList(handle, True)

    @staticmethod
    def create_from_string_list(datas: list[str | bytes]) -> "LinkedList":
        """Create an empty LinkedList"""
        handle = Wrapper.lib.LinkedList_create()
        linked_list = LinkedList(handle, True)
        for data in datas:
            linked_list.add_string(data)
        return linked_list

    @property
    def handle(self) -> LinkedListPointer:
        """Pointer to the underlying C structure"""
        return self._handle

    def add_string(self, value: str | bytes):
        """Add a string at the end of the linked list"""
        Wrapper.lib.LinkedList_add(self._handle, convert_to_bytes(value))

    def to_string_list(self) -> list[bytes]:
        """Convert a linked_list of char* to a list of string

        Returns
        -------
        list[bytes]
            _description_
        """
        result: list[bytes] = []
        current = self._handle

        while current:
            node = current.contents
            if node.data:
                value = ctypes.string_at(node.data)
                result.append(value)
            current = node.next

        return result

    def to_pointer_list(self) -> list[int]:
        """_summary_

        Returns
        -------
        list[int]
            _description_
        """

        result: list[int] = []
        current = self._handle

        while current:
            node = current.contents
            if node.data:
                value = node.data
                result.append(value)
            current = node.next

        return result
