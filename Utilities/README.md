# Utilities Directory 🛠️

A collection of helper functions used across all workshop exercises. These utilities handle common operations like object tree traversal and data processing.

## Contents

### `flatten.py`
Simple utility for flattening Speckle object trees.
```python
def flatten_base(base: Base) -> Iterable[Base]:
    """Flattens a base object into an iterable of bases."""
```

### `helpers.py`
Extended utilities for Speckle object operations:
- `speckle_print()`: Debug printing with color
- `flatten_base()`: Basic object tree flattening
- `flatten_base_thorough()`: Advanced flattening with parent tracking
- `extract_base_and_transform()`: Gets objects with transformations

### `spreadsheet.py`
Reads external configuration data:
```python
def read_rules_from_spreadsheet(url):
    """Reads TSV files for rule configuration."""
```

## Example Usage

```python
# Basic flattening
from Utilities.flatten import flatten_base
flat_objects = list(flatten_base(root_object))

# Debug printing
from Utilities.helpers import speckle_print
speckle_print("Debug message")

# Load external rules
from Utilities.spreadsheet import read_rules_from_spreadsheet
rules = read_rules_from_spreadsheet(url)
```

## Notes
- Used throughout exercises 0-3
- Handles both modern and legacy Speckle patterns
- Supports testing and debugging needs
- Manages Revit-specific data structures
