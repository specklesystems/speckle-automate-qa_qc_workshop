from typing import List, Optional, Tuple, Callable, Dict, Any, cast, Union
from specklepy.objects.base import Base
from Levenshtein import ratio
import re

# The Rules system is built as a reusable library for Speckle Automate functions.
# Key architectural principles:
#
# 1. Two-Layer Architecture:
#    - Base Rules class for generic Speckle operations
#    - Specialized RevitRules for Revit-specific needs
#    This separation allows adding other platforms (e.g., Rhino) without modifying existing code
#
# 2. Static Methods Pattern:
#    - All methods are static to avoid state management
#    - Makes testing easier as each method is independent
#    - Allows for functional composition of rules
#
# 3. Consistent Parameter Access:
#    - Handles both direct properties and nested parameters
#    - Manages legacy "@" prefixed properties
#    - Provides uniform access regardless of storage method
#
# 4. Validation Chain:
#    Start with basic existence checks -> Move to type validation -> End with value validation
#    This progression allows for early failure and clear error messages


class Rules:
    """
    Generic Speckle object validation system.
    
    This core class provides platform-agnostic validation capabilities.
    It serves as the foundation for specialized validators (like RevitRules)
    and ensures consistent behaviour across different Speckle workflows.

    Best Practices:
    - Use static methods for stateless validation
    - Handle null cases explicitly
    - Support both new and legacy property formats
    - Provide clear failure cases
    """

    @staticmethod
    def try_get_display_value(
        speckle_object: Base,
    ) -> Optional[List[Base]]:
        """Try fetching the display value from a Speckle object.

        This method encapsulates the logic for retrieving the display value from a Speckle object.
        It returns a list containing the display values if found. Otherwise, it returns None.

        Args:
            speckle_object (Base): The Speckle object from which to extract the display value.

        Returns:
            Optional[List[Base]]: A list containing the display values. If no display value is found,
                                   returns None.
        """
        # Attempt to get the display value from the speckle_object
        raw_display_value = getattr(speckle_object, "displayValue", None) or getattr(
            speckle_object, "@displayValue", None
        )

        # If no display value found, return None
        if raw_display_value is None:
            return None

        # If display value found, filter out non-Base objects
        display_values = [
            value for value in raw_display_value if isinstance(value, Base)
        ]

        # If no valid display values found, return None
        if not display_values:
            return None

        return display_values

    @staticmethod
    def is_displayable_object(speckle_object: Base) -> bool:
        """
        Determines if a given Speckle object is displayable.

        This method encapsulates the logic for determining if a Speckle object is displayable.
        It checks if the speckle_object has a display value and returns True if it does, otherwise it returns False.

        Args:
            speckle_object (Base): The Speckle object to check.

        Returns:
            bool: True if the object has a display value, False otherwise.
        """
        # Check if the speckle_object has a display value using the try_get_display_value method
        display_values = Rules.try_get_display_value(speckle_object)
        if display_values and getattr(speckle_object, "id", None) is not None:
            return True

        # Check for displayable state via definition, using try_get_display_value on the definition object
        definition = getattr(speckle_object, "definition", None)
        if definition:
            definition_display_values = Rules.try_get_display_value(definition)
            if (
                definition_display_values
                and getattr(definition, "id", None) is not None
            ):
                return True

        return False

    # Rule Generation Layer
    # These methods demonstrate how to create flexible, reusable validation rules
    # using functional programming patterns

    @staticmethod
    def speckle_type_rule(
        desired_type: str,
    ) -> Callable[[Base], bool]:
        """
        Rule factory pattern example for type checking.
        Demonstrates how to create flexible, reusable rules through closures.
        """
        return lambda prop: getattr(prop, "speckle_type", None) == desired_type

    @staticmethod
    def is_speckle_type(prop: Base, desired_type: str) -> bool:
        """
        Direct type-checking implementation.
        Provides a simpler alternative to the factory pattern for basic use cases.
        """
        return getattr(prop, "speckle_type", None) == desired_type

    # Value Validation Layer
    # These methods handle common validation scenarios in AEC workflows

    @staticmethod
    def has_missing_value(prop: Dict[str, str]) -> bool:
        """
        Rule: Missing Value Check.

        The AEC industry often requires all parameters to have meaningful values.
        This rule checks if a parameter is missing its value, potentially indicating
        an oversight during data entry or transfer.
        """
        return not prop.get("value")

    @staticmethod
    def has_default_value(prop: Dict[str, str], default="Default") -> bool:
        """
        Rule: Default Value Check.

        Default values can sometimes creep into final datasets due to software defaults.
        This rule identifies parameters that still have their default values, helping
        to highlight areas where real, meaningful values need to be provided.
        """
        return prop.get("value") == default

    @staticmethod
    def parameter_exists(prop_name: str, parent_object: Dict[str, str]) -> bool:
        """
        Rule: Parameter Existence Check.

        Their mere presence (or lack thereof) is vital for certain critical parameters.
        This rule verifies if a specific parameter exists within an object, allowing
        teams to ensure that key data points are always present.
        """
        return prop_name in parent_object.get("parameters", {})


def get_displayable_objects(flat_list_of_objects: List[Base]) -> List[Base]:
    """
    Utility function applying Rules system to filter displayable objects.
    This demonstrates how to compose Rules methods into higher-level operations.
    """
    return [
        speckle_object
        for speckle_object in flat_list_of_objects
        if Rules.is_displayable_object(speckle_object)
        and getattr(speckle_object, "id", None)
    ]

# Revit-Specific Rules Implementation
# This section implements specialized validation for Revit objects.
# The architecture handles Revit's complex parameter system including:
# - Multiple storage locations (direct properties, parameters dict, nested objects)
# - Various parameter types (built-in, shared, project, family)
# - Type vs Instance parameters
# - Value type handling and conversion

class RevitRules:
    """
    Revit-specific validation system extending base Rules capabilities.
    
    This specialized validator handles Revit's unique parameter system:
    - Built-in vs Custom parameters
    - Type vs Instance parameters
    - Project vs Family parameters
    - Shared parameters
    
    Design Philosophy:
    - Abstract away Revit parameter complexity
    - Provide consistent access patterns
    - Handle all parameter storage methods
    - Support type-safe value comparisons
    """

    @staticmethod
    def has_parameter(speckle_object: Base, parameter_name: str) -> bool:
        """
        Foundation method for parameter validation.
        
        Handles three parameter storage methods in Revit objects:
        1. Direct properties (fastest, used for built-in parameters)
        2. Parameters dictionary (common for instance parameters)
        3. Nested parameter objects (used for shared parameters)
        
        This method is the backbone of parameter validation, used by almost
        all other validation methods in the class.
        """
        if hasattr(speckle_object, parameter_name):
            return True

        parameters = cast(Base, getattr(speckle_object, "parameters", None))

        if parameters is None:
            return False

        # the parameters object can function like a dict but isn't one.
        # convert a Base object to a dict
        parameters_dict = {}

        for parameter_key in parameters.get_dynamic_member_names():
            parameters_dict[parameter_key] = getattr(parameters, parameter_key, None)

        if parameter_name in parameters_dict:
            return True

        return any(
            getattr(param_value, "name", None) == parameter_name
            for param_value in parameters_dict.values()
        )

    @staticmethod
    def get_parameter_value(
        speckle_object: Base,
        parameter_name: str,
        default_value: Any = None,
    ) -> Any | None:
        """
        Core parameter access method.
        
        This is the primary method for accessing parameter values, handling:
        - Direct property access
        - Dictionary-style parameter access
        - Nested parameter objects
        - Default value handling
        - Type conversion and validation
        
        All value-based validation methods should use this as their foundation.
        """
        # Attempt to retrieve the parameter from the root object level
        value = getattr(speckle_object, parameter_name, None)
        if value not in [None, default_value]:
            return value

        # If the "parameters" attribute is a Base object, extract its dynamic members
        parameters = getattr(speckle_object, "parameters", None)
        if parameters is None:
            return None

        # Prepare a dictionary of parameter values from the dynamic members of the parameters attribute
        parameters_dict = {
            key: getattr(parameters, key)
            for key in parameters.get_dynamic_member_names()
        }

        # Search for a direct match or a nested match in the parameters dictionary
        param_value = parameters_dict.get(parameter_name)
        if param_value is not None:
            if isinstance(param_value, Base):
                # Extract the nested value from a Base object if available
                nested_value = getattr(param_value, "value", None)
                if nested_value not in [None, default_value]:
                    return nested_value
            elif param_value not in [None, default_value]:
                return param_value

        # Use a generator to find the first matching 'value' for shared parameters stored in Base objects
        return next(
            (
                getattr(p, "value", None)
                for p in parameters_dict.values()
                if isinstance(p, Base) and getattr(p, "name", None) == parameter_name
            ),
            None,
        )

    # Value Comparison Layer
    # These methods build on the core parameter access to provide specific
    # validation rules for different comparison scenarios

    @staticmethod
    def is_parameter_value(
        speckle_object: Base, parameter_name: str, value_to_match: Any
    ) -> bool:
        """
        Exact value matching implementation.
        Foundation for simple equality-based validation rules.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        return parameter_value == value_to_match

    @staticmethod
    def is_like_parameter_value(
        speckle_object: Base,
        parameter_name: str,
        pattern: str,
        fuzzy: bool = False,
        threshold: float = 0.8,
    ) -> bool:
        """
        Pattern matching implementation supports both exact and fuzzy matching.
        It is helpful for text-based parameters where exact matches might be too strict.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        if parameter_value is None:
            return False

        if fuzzy:
            similarity = ratio(str(parameter_value), pattern)
            return similarity >= threshold
        else:
            return bool(re.match(pattern, str(parameter_value)))

    # Numeric Comparison Layer
    # Specialized methods for handling numeric parameters with type safety

    @staticmethod
    def is_parameter_value_greater_than(
        speckle_object: Base, parameter_name: str, threshold: Union[int, float]
    ) -> bool:
        """
        Type-safe numeric comparison for greater than operations.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        if parameter_value is None:
            return False
        if not isinstance(parameter_value, (int, float)):
            raise ValueError(
                f"Parameter value must be a number, got {type(parameter_value)}"
            )
        return parameter_value > threshold

    @staticmethod
    def is_parameter_value_less_than(
        speckle_object: Base, parameter_name: str, threshold: Union[int, float]
    ) -> bool:
        """
        Type-safe numeric comparison for less than operations.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        if parameter_value is None:
            return False
        if not isinstance(parameter_value, (int, float)):
            raise ValueError(
                f"Parameter value must be a number, got {type(parameter_value)}"
            )
        return parameter_value < threshold

    @staticmethod
    def is_parameter_value_in_range(
        speckle_object: Base,
        parameter_name: str,
        min_value: Union[int, float],
        max_value: Union[int, float],
        inclusive: bool = True,
    ) -> bool:
        """
        Range validation for numeric parameters.
        Supports both inclusive and exclusive range checks with type safety.
        Part of the numeric validation suite for comprehensive value checking.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        if parameter_value is None:
            return False
        if not isinstance(parameter_value, (int, float)):
            raise ValueError(
                f"Parameter value must be a number, got {type(parameter_value)}"
            )

        return (
            min_value <= parameter_value <= max_value
            if inclusive
            else min_value < parameter_value < max_value
        )

    @staticmethod
    def is_parameter_value_in_list(
        speckle_object: Base, parameter_name: str, value_list: List[Any]
    ) -> bool:
        """
        List membership validation.
        It is important for checking against predefined valid values,
        common in Revit for enumerated parameters.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        return parameter_value in value_list

    # Boolean Parameter Layer
    # Specialized handling for boolean parameters, common in Revit
    # for yes/no properties and switches

    @staticmethod
    def is_parameter_value_true(speckle_object: Base, parameter_name: str) -> bool:
        """
        Boolean validation for true values.
        Used for confirming positive states in yes/no parameters.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        return parameter_value is True

    @staticmethod
    def is_parameter_value_false(speckle_object: Base, parameter_name: str) -> bool:
        """
        Boolean validation for false values.
        Used for confirming negative states in yes/no parameters.
        """
        parameter_value = RevitRules.get_parameter_value(speckle_object, parameter_name)
        return parameter_value is False

    # Category Management Layer
    # These methods handle Revit's category system, which is fundamental
    # to object organization and filtering in Revit workflows

    @staticmethod
    def has_category(speckle_object: Base) -> bool:
        """
        Category existence check.
        Foundational method for category-based filtering and validation.
        """
        return RevitRules.has_parameter(speckle_object, "category")

    @staticmethod
    def is_category(speckle_object: Base, category_input: str) -> bool:
        """
        Category matching implementation.
        The core method is for filtering objects by their Revit category.
        """
        category_value = RevitRules.get_parameter_value(speckle_object, "category")
        return category_value == category_input

    @staticmethod
    def get_category_value(speckle_object: Base) -> str:
        """
        Category value retrieval.
        Helper method for accessing category information directly.
        """
        return RevitRules.get_parameter_value(speckle_object, "category")


# Utility Layer
# High-level operations that compose multiple rules for common workflows

def filter_objects_by_category(
    speckle_objects: List[Base], category_input: str
) -> Tuple[List[Base], List[Base]]:
    """
    High-level category filtering operation.
    
    This utility demonstrates how to compose RevitRules methods into
    practical workflows. It separates objects into matching and non-matching
    groups for easier processing.
    
    Design Pattern:
    - Takes a list of objects and a single criterion
    - Returns two lists (matching and non-matching)
    - Uses RevitRules for consistent validation
    - Maintains clear separation of concerns
    """
    matching_objects = []
    non_matching_objects = []

    for speckle_object in speckle_objects:
        if RevitRules.is_category(speckle_object, category_input):
            matching_objects.append(speckle_object)
        else:
            non_matching_objects.append(speckle_object)

    return matching_objects, non_matching_objects
