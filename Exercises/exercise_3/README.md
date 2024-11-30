# Exercise 3: Externalised Configuration 📊

This exercise builds upon the framework established in Exercise 2 by introducing externalised rule configuration. By moving from hardcoded validation logic to an external, editable format, we reduce the dependency on developers, enable non-technical stakeholders to participate, and create a scalable, flexible QAQC system.

## Key Changes from Exercise 2 📈

In **Exercise 2**, rules were **hardcoded** directly into the Python codebase. While this approach works well for specific use cases, it has significant drawbacks:

### Limitations of Hardcoded Rules:
1. **Workflow-Specific but Inflexible**:
   - Hardcoding rules tightly couple them to a single workflow, making them less adaptable for new requirements.
   - Developers become a bottleneck; they must modify, test, and redeploy code for minor changes.

2. **High Friction to Change**:
   - Every rule change requires developer intervention and redeployment.
   - Non-technical users need a direct way to update rules, creating inefficiencies and delays.
  

### Improvements in Exercise 3:
1. **Separation of Rules from Code**:
   - Rules are now stored in a spreadsheet, allowing easy updates without touching the code.
   - This separation simplifies testing, maintenance, and auditing.

2. **User Empowerment**:
   - Non-developers can modify rules directly in the spreadsheet, significantly lowering the friction for changes.

3. **Scalability and Reusability**:
   - The system is now flexible enough to handle diverse workflows by simply swapping or updating the spreadsheet.

    #### Input Schema Changes
    ```python
    class FunctionInputs(AutomateBase):
      spreadsheet_url: str = Field(
          title="Spreadsheet URL",
          description="URL of the spreadsheet containing validation rules."
      )
    ```

    #### Rule Processing System
    ```python
    def apply_rules_to_objects(
        speckle_objects: List[Base],
        rules_df: pd.DataFrame,
        automate_context: AutomationContext,
    ) -> dict[str, Tuple[List[Base], List[Base]]]:
        # Rule application logic
    ```
By externalising configuration, we address Exercise 2's inflexibility and scalability issues while retaining the ability to hardcode specific rules when needed for a particular workflow.

## Spreadsheet Structure 🗂️

The spreadsheet serves as a rule definition template. 

### Example Rule:

| Rule Number | Logic | Property Name      | Predicate     | Value        | Message                                  | Report Severity |
|-------------|-------|--------------------|---------------|--------------|------------------------------------------|-----------------|
| 1           | WHERE | category           | matches       | Walls        | SPECKLE_Classification must exist.       | Error           |
| 2           | AND   | height             | greater than  | 1200         | Wall height must exceed 1200mm.          | Error           |

It consists of the following columns:

| **Column**         | **Description**                                                                 |
|---------------------|---------------------------------------------------------------------------------|
| **Rule Number**     | Groups related rules under a unique identifier.                                |
| **Logic**           | Specifies the logical operator (`WHERE` for filters, `AND` for conditions).    |
| **Property Name**   | The parameter or property to validate (e.g., `height`, `category`).            |
| **Predicate**       | The operator for comparison (e.g., `greater than`, `matches`, `exists`).       |
| **Value**           | The target value or reference for the predicate (e.g., `1200`, a category name).|
| **Message**         | Feedback displayed when a rule is triggered.                                   |
| **Report Severity** | Categorises results as `Error` or `Warning` based on priority.                 |

## Publishing the Spreadsheet 🌐

To enable the automation function to access your spreadsheet:

1. **Make a copy** of the provided template.
2. **Edit the rules** in the specified format.
3. **Publish as TSV (Tab-Separated Values)**:
   - Open your spreadsheet.
   - Go to **File > Share > Publish to the Web**.
   - Choose **Tab-separated values (.tsv)** as the format.
   - Copy the generated URL.
4. **Input the URL** into the automation function’s input field.

## Validation Framework Overview 🛠️

### Process Flow:
1. **Load Rules**:
   - The function fetches the rules from the spreadsheet using the provided URL.
2. **Parse Rules**:
   - Rules are dynamically interpreted and grouped based on `Rule Number`.
3. **Apply Rules**:
   - Objects in the Speckle model are evaluated against each rule’s conditions.
4. **Report Results**:
   - Issues are categorised as `Warnings` or `Errors`, with detailed feedback provided in the Speckle viewer.

### Benefits of the Framework:
- **Flexibility**: Switch rules without modifying code.
- **Transparency**: Rules are visible and auditable in the spreadsheet.
- **User-Focused**: Enables non-technical stakeholders to participate in defining standards.

## File Breakdown 🗃️

1. **`function.py`**:
   - Implements the automation logic and integrates external rule definitions.
   - Validates objects based on the spreadsheet configuration.

2. **`inputs.py`**:
   - Defines the input schema, requiring only the URL of the spreadsheet.

3. **`rules.py`**:
   - Contains logic for evaluating rules and applying predicates to objects.

4. **Spreadsheet (TSV)**:
   - An adaptable, external data source for defining validation logic.

## Testing 🧪

After configuring your spreadsheet:

1. Run the function locally with test data to verify the rule application:
   ```bash
   pytest tests/local_test_exercise3.py::test_function_run

2. Validate the feedback messages and ensure results align with expectations.

## Why Keep Hardcoded Rules?
While externalised rules improve flexibility and scalability, some use cases may still benefit from hardcoded logic:

- Highly Specific Workflows: Certain validations may be too unique or intricate to generalise in a spreadsheet.
- Performance Considerations: Directly coding rules might optimise performance for frequently executed validations.

Combining both approaches, Exercise 3 offers the best of both worlds: the flexibility of externalised configuration and the precision of hardcoded rules.



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
