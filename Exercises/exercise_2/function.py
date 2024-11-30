from speckle_automate import AutomationContext
from Utilities.helpers import flatten_base, speckle_print
from Workshop.Exercise_2.inputs import FunctionInputs
from Workshop.Exercise_2.rules import RevitRules, filter_objects_by_category


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """Exercise 2: Property validation for categorized Revit objects.
    
    This completely new implementation replaces the random comment functionality 
    from Exercise 1 with systematic property validation. The key differences include:
    
    1. Instead of adding random comments, it validates specific properties on objects
    2. Filters objects by Revit category instead of just displayable objects
    3. Implements property validation using the new RevitRules system
    4. Provides detailed reporting on property status with error/warning/info markers
    
    Architecture Note:
    This implementation demonstrates best practices by utilizing external Rules classes 
    (Rules and RevitRules). These classes form part of a reusable code library that can be 
    shared across multiple Speckle Automate functions. This approach:
    - Promotes code reuse and consistency across automation tasks
    - Reduces duplication of common validation logic
    - Creates a private library of tested, reliable utilities
    - Makes automation functions cleaner and more focused on their specific tasks
    - Allows for centralized updates to validation logic
    
    Args:
        automate_context: A context-helper object that carries relevant information
            about the runtime context of this function.
            It gives access to the Speckle project data that triggered this run.
            It also has convenient methods for attaching result data to the Speckle model.
        function_inputs: An instance object matching the defined schema.
            Now includes:
            - category: The Revit category to check
            - property: The property name to validate
    """
    # Get the version root object
    version_root_object = automate_context.receive_version()

    # Get flattened list of objects
    flat_list_of_objects = list(flatten_base(version_root_object))

    # Use the new filter_objects_by_category function from our reusable rules library
    in_category_objects, non_category_objects = filter_objects_by_category(
        flat_list_of_objects, 
        function_inputs.category
    )

    # Categorize objects based on property existence and validity
    non_property_objects = []
    property_objects = []
    valid_property_objects = []
    invalid_property_objects = []

    # Process each object using rules from our reusable library
    for obj in in_category_objects:
        if not RevitRules.has_parameter(obj, function_inputs.property):
            non_property_objects.append(obj)
        else:
            property_objects.append(obj)
            param_value = RevitRules.get_parameter_value(obj, function_inputs.property)
            if param_value not in ["", "Default", None]:
                valid_property_objects.append(obj)
                speckle_print(param_value)  # Print valid values
            else:
                invalid_property_objects.append(obj)

    # Attach results to objects
    if non_property_objects:
        automate_context.attach_error_to_objects(
            category=f"Missing Property {function_inputs.category} Objects",
            object_ids=[obj.id for obj in non_property_objects],
            message=f"This {function_inputs.category} does not have the specified property {function_inputs.property}",
        )

    if invalid_property_objects:
        automate_context.attach_warning_to_objects(
            category=f"Invalid Property {function_inputs.category} Objects",
            object_ids=[obj.id for obj in invalid_property_objects],
            message=f"This {function_inputs.category} has the specified property {function_inputs.property} but it is empty or default",
        )

    if valid_property_objects:
        automate_context.attach_info_to_objects(
            category=f"Valid Property {function_inputs.category} Objects",
            object_ids=[obj.id for obj in valid_property_objects],
            message=f"This {function_inputs.category} has valid values for the property {function_inputs.property}",
        )

    # Mark overall run status with detailed counts
    total_objects = len(in_category_objects)
    if len(non_property_objects) > 0:
        automate_context.mark_run_failed(
            f"Found {len(non_property_objects)} objects without the required property out of {total_objects} total {function_inputs.category} objects."
        )
    elif len(invalid_property_objects) > 0:
        automate_context.mark_run_success(
            f"Found {len(invalid_property_objects)} objects with empty/default values out of {total_objects} total {function_inputs.category} objects."
        )
    else:
        automate_context.mark_run_success(
            f"All {total_objects} {function_inputs.category} objects have valid {function_inputs.property} properties."
        )

    # Reset view
    automate_context.set_context_view()
