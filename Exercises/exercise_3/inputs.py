from pydantic import Field
from speckle_automate import AutomateBase

class FunctionInputs(AutomateBase):
    """These are function author-defined values.
    
    Exercise 3 demonstrates how to externalize configuration by moving validation rules
    to an external data source (spreadsheet). This allows non-developers to modify rules
    without changing code, enabling easier validation logic maintenance and updates.
    
    The previous exercise had rules hardcoded in the Python files. Now, we only need
    a single input - the URL of the spreadsheet containing the rules.
    """
    spreadsheet_url: str = Field(
        title="Spreadsheet URL",
        description="This is the URL of the spreadsheet containing validation rules. "
                   "The spreadsheet should be in TSV (tab-separated values) format and "
                   "contain columns for Rule Number, Property Name, Predicate, Value, "
                   "Message, and Report Severity.",
    )
