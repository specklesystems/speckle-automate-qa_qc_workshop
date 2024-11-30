import random

from speckle_automate import AutomationContext

from Exercises.exercise_1.inputs import FunctionInputs
from Utilities.flatten import flatten_base


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """This is an example Speckle Automate function.

    Args:
        automate_context: A context helper object, that carries relevant information
            about the runtime context of this function.
            It gives access to the Speckle project data, that triggered this run.
            It also has convenience methods attach result data to the Speckle model.
        function_inputs: An instance object matching the defined schema.
    """

    # No change: Get the root object from the context
    version_root_object = automate_context.receive_version()

    # CHANGE: Convert generator to list for better handling
    # This allows us to reuse the flat_list_of_objects multiple times
    flat_list_of_objects = list(flatten_base(version_root_object))

    # No change: Basic displayable object filtering
    displayable_objects = [
        speckle_object
        for speckle_object in flat_list_of_objects
        if (
            getattr(speckle_object, "displayValue", None)
            or getattr(speckle_object, "@displayValue", None)
        )
        and getattr(speckle_object, "id", None) is not None
    ]

    # NEW: Enhanced displayable object detection
    # Now also includes instance objects that have displayable definitions
    # This provides better support for more complex Speckle object structures
    displayable_objects += [
        instance_object
        for instance_object in flat_list_of_objects
        if (
            getattr(instance_object, "definition", None)
            and (
                (
                    getattr(
                        getattr(instance_object, "definition"), "displayValue", None
                    )
                    or getattr(
                        getattr(instance_object, "definition"), "@displayValue", None
                    )
                )
                and getattr(getattr(instance_object, "definition"), "id", None)
                is not None
            )
        )
    ]

    if len(displayable_objects) == 0:
        # No change: Handle case when no displayable objects are found
        automate_context.mark_run_failed(
            "Automation failed: No displayable objects found."
        )

    else:
        # MAJOR CHANGE: Multiple object selection
        # Instead of selecting just one random object, we now select multiple objects
        # based on the user-specified number_of_elements
        real_number_of_elements = min(
            function_inputs.number_of_elements,  # User requested amount
            len(displayable_objects),            # Available amount
        )

        # NEW: Using random.sample instead of random.choice
        # This allows selection of multiple unique objects
        selected_objects = random.sample(
            displayable_objects,
            real_number_of_elements,
        )

        # NEW: Create list of object IDs for batch processing
        selected_object_ids = [obj.id for obj in selected_objects]

        # MODIFIED: Attach comments to multiple objects
        # Now operates on all selected objects instead of just one
        comment_message = f"{function_inputs.comment_phrase}"
        automate_context.attach_info_to_objects(
            category="Selected Objects",
            object_ids=selected_object_ids,
            message=comment_message,
        )

        # NEW: Visual feedback enhancement
        # Added gradient visualization to help users identify selected objects
        # Each object gets a sequential gradient value for visual distinction
        gradient_values = {
            object_id: {"gradientValue": index + 1}
            for index, object_id in enumerate(selected_object_ids)
        }

        # NEW: Attach gradient visualization data
        automate_context.attach_info_to_objects(
            category="Index Visualisation",
            metadata={
                "gradient": True,
                "gradientValues": gradient_values,
            },
            message="Object Indexes",
            object_ids=selected_object_ids,
        )

        # MODIFIED: Updated success message
        # Now includes the actual number of objects processed
        automate_context.mark_run_success(
            f"Added comment to {real_number_of_elements} random objects."
        )

    # No change: Maintain original view context
    automate_context.set_context_view()
