import sys
from ctypes import CDLL, cdll

from .common import linked_list
from .iec61850 import (
    cdc,
    client,
    config_file_parser,
    dynamic_model,
    iec61850_common,
    model,
    server,
)
from .mms import mms_value


class _Wrapper:

    def __init__(self) -> None:
        self._libiec61850 = None

    def load_library(self, name: str | None = None):

        if name is None:
            name = "./libiec61850.so" if sys.platform != "win32" else "./iec61850.dll"

        _libiec61850 = cdll.LoadLibrary(name)

        # Common
        linked_list.setup_prototypes(_libiec61850)
        # IEC61850
        cdc.setup_prototypes(_libiec61850)
        client.setup_prototypes(_libiec61850)
        config_file_parser.setup_prototypes(_libiec61850)
        dynamic_model.setup_prototypes(_libiec61850)
        iec61850_common.setup_prototypes(_libiec61850)
        model.setup_prototypes(_libiec61850)
        server.setup_prototypes(_libiec61850)
        # MMS
        mms_value.setup_prototypes(_libiec61850)

        self._libiec61850 = _libiec61850

    @property
    def lib(self) -> CDLL:
        if self._libiec61850 is None:
            self.load_library()
        return self._libiec61850  # type:ignore


Wrapper = _Wrapper()
