from pydantic import Field, constr
from speckle_automate import AutomateBase


class FunctionInputs(AutomateBase):
    """These are function author defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    comment_phrase: constr(min_length=1, max_length=500) = Field(
        title="Comment Phrase",
        description="This phrase will be added to a random model element.",
        example="This is a sample comment."
    )
