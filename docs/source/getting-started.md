# Getting started

## Installation

To install this python module, you can install from git with the folliwng command

```bash
pip install git+https://github.com/etihwo/py61850.git
```

Before using the module you need to have the [libiec61850](https://github.com/mz-automation/libiec61850) shared library on your computer. You can refere to one of the following option to retrieve it.

- download from the latest release from <https://github.com/etihwo/libiec61850> which are compiled without any optional features.
- refer to the [official documentation](https://github.com/mz-automation/libiec61850)
- compile the libiec61850 library as explained below

### Compilation of libiec61850

First clone the repo and go in the folder.

```shell
git clone https://github.com/mz-automation/libiec61850.git
cd libiec61850
```

Compilation step for Linux:

```shell
mkdir -p build
cd build
cmake ..
make iec61850-shared
```

Compilation step for Windows:

```shell
mkdir -p build
cd build
cmake -G "Visual Studio 17 2022" -A x64 ..
cmake --build . --config Release
```

Please refer to the [official documentation](https://github.com/mz-automation/libiec61850) to install optional features.

## Configuration

Once the module is installed and shared library is compiled, you can put the shared library in your current folder. Then you can use the python module.

If the name of the library is not `libiec61850.so` for linux or `iec61850.dll` for windows or if you put the shared library in an other folder, you have to use the following code to locate and load the library.

```python
from py61850.binding.loader import Wrapper
Wrapper.load_library("path to the .so or .dll")
```
