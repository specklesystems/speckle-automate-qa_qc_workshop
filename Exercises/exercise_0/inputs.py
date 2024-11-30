from pydantic import Field
from speckle_automate import AutomateBase


class FunctionInputs(AutomateBase):
    """These are function author defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    comment_phrase: str = Field(
      title="Comment Phrase",
      description="This phrase will be added to a random model element.",
    )
