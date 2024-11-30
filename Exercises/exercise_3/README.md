# Exercise 3: Externalized Configuration 📊

This exercise demonstrates how to move validation rules from code to external configuration, making the system more maintainable and user-friendly.

## What's New ✨
1. External rule configuration via spreadsheet
2. Enhanced rule processing system
3. More flexible validation framework
4. Improved reporting and feedback

## Key Changes from Exercise 2 📈

### Input Schema Changes
```python
class FunctionInputs(AutomateBase):
    spreadsheet_url: str = Field(
        title="Spreadsheet URL",
        description="URL of the spreadsheet containing validation rules"
    )
```

### Rule Processing System
```python
def apply_rules_to_objects(
    speckle_objects: List[Base],
    rules_df: pd.DataFrame,
    automate_context: AutomationContext,
) -> dict[str, Tuple[List[Base], List[Base]]]:
    # Rule application logic
    ...
```

## System Architecture 🏗️

### Spreadsheet Structure
| Rule Number | Property Name | Predicate | Value | Message | Report Severity |
|------------|---------------|-----------|--------|---------|-----------------|
| 1          | Height        | greater than | 2.5    | Height check | Warning        |
| 2          | Material      | exists    | -      | Material required | Error         |

### Rule Processing Flow
1. Load rules from spreadsheet
2. Parse and validate rule definitions
3. Apply rules to objects
4. Generate comprehensive results
5. Report outcomes with appropriate severity

## Key Learning Points 📝
- [ ] Separating configuration from code
- [ ] Building flexible rule processors
- [ ] Working with external data sources
- [ ] Creating maintainable automation systems
- [ ] Implementing complex validation logic
- [ ] Enhanced error handling and reporting

## Testing 🧪
Run the test file:
```bash
pytest tests/local_test_exercise3.py::test_function_run
```
