# Local Testing Guide for Speckle Automate Functions

This guide explains how to set up and run local tests for your Speckle Automate functions, allowing you to validate your automation logic before deployment.

## Prerequisites

Before running local tests, you'll need:

1. A Speckle project where you can create test automations
2. A test automation set up in your project
3. A Personal Access Token (PAT) from Speckle
4. Your project and automation IDs from the test automation URL

## Environment Setup

### 1. Create Environment Variables

Create a `.env` file in your project root with the following variables:

```env
SPECKLE_TOKEN=your_personal_access_token
SPECKLE_SERVER_URL=https://app.speckle.systems
SPECKLE_PROJECT_ID=your_project_id
SPECKLE_AUTOMATION_ID=your_automation_id
```

### 2. Test Configuration

The repository includes a `conftest.py` that loads these environment variables for testing:

```python
import os
from dotenv import load_dotenv

def pytest_configure(config):
    load_dotenv(dotenv_path=".env")
    
    token_var = "SPECKLE_TOKEN"
    server_var = "SPECKLE_SERVER_URL"
    # ... validation logic ...
```

## Running Tests

### Test Structure

Each exercise has its own test file (e.g., `local_test_exercise0.py`). The tests:
1. Initialize an automation context
2. Run the function with test inputs
3. Validate the results

Example test structure:
```python
def test_function_run(test_automation_run_data, test_automation_token):
    automation_context = AutomationContext.initialize(
        test_automation_run_data, test_automation_token
    )
    automate_sdk = run_function(
        automation_context,
        automate_function,
        FunctionInputs(comment_phrase="Test Comment")
    )
    assert automate_sdk.run_status == AutomationStatus.SUCCEEDED
```

### Running Individual Tests

To run tests for a specific exercise:

```bash
# Exercise 0
pytest tests/local_test_exercise0.py::test_function_run

# Exercise 1
pytest tests/local_test_exercise1.py::test_function_run

# Exercise 2
pytest tests/local_test_exercise2.py::test_function_run

# Exercise 3
pytest tests/local_test_exercise3.py::test_function_run
```

## Test Automation Setup

1. Navigate to your project's Automations tab
2. Click "New Automation"
3. Select "Create Test Automation" in the bottom left
4. Follow the configuration steps

> **Note**: You must be a project owner and have published your function to create test automations.

## Understanding Test Results

Test runs provide insights into:
- Function execution success/failure
- Business logic validation
- Interaction with Speckle project data
- Result generation and attachment

Results can be viewed:
- In your terminal during test execution
- On the automation page in your Speckle project
- In the project's automation status display

## Additional Resources

For more detailed information about testing Speckle Automate functions, see:
- [Function Testing Documentation](https://speckle.guide/automate/function-testing.html)
- Python SDK Documentation
- Example Function Repositories

## Limitations and Notes

- Test automations require you to be a project owner
- The function must be published with at least one release
- Test automations run in a sandbox environment
- Function inputs are set in your development environment, not the UI
- Future updates may add restrictions on test automation ownership

## Troubleshooting

If you encounter issues:
1. Verify your environment variables are correctly set
2. Ensure your PAT has the necessary permissions
3. Check that your test automation is properly configured
4. Validate your function inputs match the expected schema

For additional help, refer to the Speckle documentation or contact support.
