# Exercise 2: Property Validation 🔍

This exercise represents a significant shift from random comments to systematic property validation, introducing a robust rules system.

## What's New ✨
1. Complete rewrite focusing on property validation
2. Introduction of the RevitRules system
3. Category-based object filtering
4. Comprehensive property validation framework

## Key Changes from Exercise 1 📈

### Input Schema Changes
```python
class FunctionInputs(AutomateBase):
    category: str = Field(
        title="Revit Category",
        description="The category of objects to validate"
    )
    property: str = Field(
        title="Property Name",
        description="The property to check"
    )
```

### RevitRules System
```python
class RevitRules:
    @staticmethod
    def has_parameter(speckle_object: Base, parameter_name: str) -> bool:
        # Parameter validation logic
        ...

    @staticmethod
    def get_parameter_value(speckle_object: Base, parameter_name: str) -> Any:
        # Parameter value retrieval logic
        ...
```

## Core Components 🔧

### Validation Process
1. Filter objects by category
2. Check property existence
3. Validate property values
4. Report results with appropriate severity

### Result Types
- ✅ Info: Valid properties
- ⚠️ Warning: Empty/default values
- ❌ Error: Missing properties

## Key Learning Points 📝
- [ ] Building reusable validation systems
- [ ] Working with Revit categories and properties
- [ ] Implementing complex filtering logic
- [ ] Creating hierarchical rule structures
- [ ] Managing different types of validation results

## Testing 🧪
Execute the test file:
```bash
pytest tests/local_test_exercise2.py::test_function_run
```
