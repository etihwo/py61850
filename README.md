# py61850

A Python module for interfacing with the libiec61850 C library, enabling communication with devices using the IEC 61850 protocol.

## Installation and configuration

```bash
pip install git+https://github.com/etihwo/py61850.git
```

This module requires the native libiec61850 library. By default, the module assume that the shared library files (iec61580.so on Linux, iec61580.dll on Windows) is on the current folder.

Before using the module, you can set the path to the shared library with:

```python
from py61850.binding.loader import Wrapper
Wrapper.load_library("./iec61580.dll")
```

## Features

- Connect to IEC 61850 servers via MMS
- Read and write Data Attributes (DA)
- Navigate logical device structures (LD, LN, DO, DA)
- Robust error handling and timeout management
- Support for complex and nested data types

## Dependencies

- Python ≥ 3.8
- libiec61850 (https://github.com/mz-automation/libiec61850)
- ctypes (standard Python library)

## Documentation

Full API documentation is available in the docs/ folder and can be generated using Sphinx. It is also available on https://etihwo.github.io/py61850/

## Technical Notes

This module uses ctypes to wrap the C functions exposed by libiec61850. It handles type conversions, pointer management, and structure mapping to provide a clean Pythonic interface.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
1. Create a feature branch
1. Submit a pull request

## License

This project is licensed under the GPLv3 License. See the `LICENSE` file for details.
