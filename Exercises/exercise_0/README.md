# Exercise 0: Basic Automation 🚀

This exercise introduces the fundamental concepts of Speckle Automate by implementing a simple random comment function. It's based on the root `main.py` template.

## Key Components 🔑

### Inputs (`inputs.py`)
```python
comment_phrase: str = Field(
    title="Comment Phrase",
    description="This phrase will be added to a random model element."
)
```
- Single input parameter: `comment_phrase`
- Uses Pydantic for input validation
- Demonstrates basic input schema definition

### Function (`function.py`)
```python
def automate_function(automate_context: AutomationContext, function_inputs: FunctionInputs) -> None:
    # Get the version's root object
    version_root_object = automate_context.receive_version()

    # Get displayable objects, add comment to random one
    # ...
```
Demonstrates use of the AutomateContext for:
- Loading model data
- Attaching comments
- Setting view state
- Handling success/failure states

## Function Flow 📊
1. Receives the version's root object
2. Flattens the object tree
3. Filters for displayable objects
4. Randomly selects one object
5. Attaches a comment to the selected object
6. Reports success or failure

## Key Learning Points 📝
- [ ] Understanding basic Automate function structure
- [ ] Working with Speckle objects and their properties
- [ ] Using AutomateContext for model interaction
- [ ] Basic error handling and status reporting

## Testing 🧪
Use the provided test file:
```bash
pytest tests/local_test_exercise0.py::test_function_run
```
