import random

from speckle_automate import AutomationContext

from Exercises.exercise_0.inputs import FunctionInputs
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

    # the context provides a convenient way, to receive the triggering version
    version_root_object = automate_context.receive_version()

    flat_list_of_objects = flatten_base(version_root_object)

    # filter the list to only include objects that are displayable.
    # this is a simple example, that checks if the object has a displayValue
    displayable_objects = [
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

        print(len(displayable_objects))

    else:
        # select a random object from the list
        random_object = random.choice(displayable_objects)

        automate_context.attach_info_to_objects(
          category="Selected Object",
          object_ids=[random_object.id],
          message=function_inputs.comment_phrase,
        )

        automate_context.mark_run_success("Added a comment to a random object.")

    # set the automation context view, to the original model / version view
    automate_context.set_context_view()
