"""Run integration tests with a speckle server."""

from speckle_automate import (
  AutomationContext,
  AutomationRunData,
  AutomationStatus,
  run_function
)

from main import FunctionInputs, automate_function

from speckle_automate.fixtures import *


def test_function_run(test_automation_run_data: AutomationRunData, test_automation_token: str):
    """Run an integration test for the automate function."""
    automation_context = AutomationContext.initialize(
      test_automation_run_data, test_automation_token
    )
    automate_sdk = run_function(
      automation_context,
      automate_function,
      FunctionInputs(
        comment_phrase="Bananagram."
      ),
    )

    assert automate_sdk.run_status == AutomationStatus.SUCCEEDED

# cli command to run just this test with pytest: pytest tests/local_test.py::test_function_run
