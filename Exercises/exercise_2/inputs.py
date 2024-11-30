from pydantic import Field
from speckle_automate import AutomateBase

class FunctionInputs(AutomateBase):
    """Input parameters for the Revit property validation function."""
    
    # Category of Revit elements to check
    category: str = Field(
        title="Revit Category",
        description="The category of objects to validate (e.g., Walls, Floors)",
    )
    
    # Property to validate within the category
    property: str = Field(
        title="Property Name",
        description="The property to check on each object in the category",
    )
