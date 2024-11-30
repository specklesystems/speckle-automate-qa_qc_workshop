import random
from typing import List
from speckle_automate import AutomationContext
from specklepy.objects import Base
from Exercises.exercise_0.inputs import FunctionInputs
from Utilities.flatten import flatten_base


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """Attaches a comment to a randomly selected displayable object in the model.
    
    Flattens the object tree, filters for displayable objects (those with a displayValue 
    and id), randomly selects one, and attaches the input comment phrase to it.
    
    Args:
        automate_context: Provides access to the Speckle project data and methods
            for attaching results.
        function_inputs: Contains the comment phrase to attach to the selected object.
    """
    # Get the version's root object
    version_root_object = automate_context.receive_version()

    # Flatten the object tree
    flat_list_of_objects: List[Base] = flatten_base(version_root_object)

    # Filter for displayable objects that have visual representation in the viewer
    # We do this because:
    # 1. Only displayable objects will be visible to users in the Speckle viewer
    # 2. Some objects are just containers or metadata and shouldn't receive comments
    # 3. We need objects with IDs to be able to attach comments to them
    # 4. This ensures users can see the objects we're commenting on
    displayable_objects: List[Base] = [
        speckle_object
        for speckle_object in flat_list_of_objects
        if (
            getattr(speckle_object, "displayValue", None)
            or getattr(speckle_object, "@displayValue", None)
        ) and getattr(speckle_object, "id", None) is not None
    ]

    if len(displayable_objects) == 0:
        automate_context.mark_run_failed(
            "Automation failed: No displayable objects found."
        )
    else:
        # Select and comment on random object
        random_object = random.choice(displayable_objects)
        
        automate_context.attach_info_to_objects(
            category="Selected Object",
            object_ids=[random_object.id],
            message=function_inputs.comment_phrase,
        )

        automate_context.mark_run_success("Added a comment to a random object.")

    # Reset view to original
    automate_context.set_context_view()
