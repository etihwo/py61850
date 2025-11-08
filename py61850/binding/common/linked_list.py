"""Module for C binding with common/inc/linked_list.h"""

from ctypes import CDLL, POINTER, Structure, c_void_p


class SLinkedList(Structure):
    pass


SLinkedList._fields_ = [("data", c_void_p), ("next", POINTER(SLinkedList))]
LinkedList = POINTER(SLinkedList)


def setup_prototypes(lib: CDLL):
    """Add prototypes definition to the lib"""

    lib.LinkedList_create.argtypes = []
    lib.LinkedList_create.restype = LinkedList

    lib.LinkedList_destroy.argtypes = [
        LinkedList,  # LinkedList self
    ]
    lib.LinkedList_destroy.restype = None

    lib.LinkedList_add.argtypes = [
        LinkedList,  # LinkedList self
        c_void_p,  # void* data
    ]
    lib.LinkedList_add.restype = None
