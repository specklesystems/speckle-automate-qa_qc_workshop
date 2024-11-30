from speckle_automate import AutomationContext
from Utilities.helpers import flatten_base, speckle_print
from Utilities.spreadsheet import read_rules_from_spreadsheet
from .inputs import FunctionInputs
from .rules import apply_rules_to_objects

def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """Exercise 3: Externalized Configuration
    
    This exercise demonstrates how to move from hardcoded rules to externally configured
    validation rules. The key improvements from Exercise 2 are:
    
    1. Configuration is separated from code:
       - Rules are stored in an external spreadsheet
       - Business users can modify rules without developer involvement
       - Rules can be updated without redeploying code
    
    2. More flexible rule structure:
       - Rules can be grouped together
       - Multiple conditions can be combined
       - Different severity levels can be specified
       - Custom messages can be provided for each rule
       
    3. Better maintainability:
       - Rules are more accessible to review and audit
       - Changes can be tracked in the spreadsheet
       - Rules can be version-controlled separately from code
       
    Args:
        automate_context: Provides access to the Speckle project data and methods
            for attaching results.
        function_inputs: Contains the URL to the rules spreadsheet.
    """
    # Get the version root object as before
    version_root_object = automate_context.receive_version()
    
    # Flatten the object tree into a processable list
    flat_list_of_objects = list(flatten_base(version_root_object))
    
    # Read validation rules from the external spreadsheet
    # This replaces the hardcoded rules from Exercise 2
    rules = read_rules_from_spreadsheet(function_inputs.spreadsheet_url)
    if rules is None or rules.empty:
        automate_context.mark_run_failed("Failed to read rules from spreadsheet")
        return
        
    # Apply all rules to the objects and collect results
    # The rules system is now more sophisticated, supporting:
    # - Rule grouping
    # - Multiple conditions
    # - Different severity levels
    # - Custom success/failure messages
    results = apply_rules_to_objects(flat_list_of_objects, rules, automate_context)
    
    # Calculate summary statistics to show the scope of validation
    total_rules = len(results)
    total_objects = len(flat_list_of_objects)
    objects_validated = sum(len(passes) + len(fails) for passes, fails in results.values())
    
    # Reset view to original model state
    automate_context.set_context_view()
    
    # Provide a detailed summary of the validation results
    automate_context.mark_run_success(
        f"Successfully applied {total_rules} rules to {objects_validated} objects "
        f"out of {total_objects} total objects."
    )
