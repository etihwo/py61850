# Contributor Guide

## Development Workflow

- Go to https://github.com/etihwo/py61850 and click the "fork" button to create your own copy of the project.
- Clone the project to your local computer:

```shell
git clone https://github.com/<Your Username Here>/py61850
```

- Next, you need to set up your build environment:
  - Here are instructions for vscode:
    - Open the folder with vscode
    - Install the recommended extension at least the [ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - Run the `Python: Create Environnement...`
    - Select the optional dependency for `docs`, `dev`, and `test`
- Finally, we recommend you install pre-commit which checks that your code matches formatting guidelines:

```shell
pre-commit install
```

## Guidelines

- All code should have tests.
- All code should be documented, to the same [standard](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard) as NumPy and SciPy.
