from pydantic import Field
from speckle_automate import AutomateBase


class FunctionInputs(AutomateBase):
    """These are function author defined values.
    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    # In this exercise, we will add two new input fields to the FunctionInputs class.
    category: str = Field(
      title="Revit Category",
      description="This is the category objects to check.",
    )
    property: str = Field(
      title="Property Name",
      description="This is the property to check.",
    )
