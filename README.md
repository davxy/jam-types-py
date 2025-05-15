# JAM Types

Support Types for JAM Graypaper v0.6.5

## Install

First, create a virtual environment in the desired location.

```bash
python -m venv ~/.local/pip/jam-types-tiny
```

Activate the virtual environment to install the package inside it.

```bash
source ~/.local/pip/jam-types-tiny/bin/activate
```

Once the virtual environment is activated, you can install the package using
`pip`.

```bash
pip install .  
```

By default, types for the `tiny` node variant are installed. If you wish to
install types for the `full` node variant, please first modify the
[const](./jam_types/const.py) sources accordingly.
