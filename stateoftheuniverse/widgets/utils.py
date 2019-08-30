"""
Utility function for widgets.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

from typing import Callable


# -----------------------------------------------------------------------------
# FUNCTION DEFINITIONS
# -----------------------------------------------------------------------------

def stringdecorator(function: Callable) -> Callable:
    """
    Decorator function which can be used to easily add dashed lines,
    name, etc. to the `get_string()` method of a widget.

    Args:
        function: The function to be decorated. Generally, this will
            be the `get_string()` method of a widget.

    Returns:
        The decorated `function`.
    """

    def wrapper(*args):
        self = args[0]
        string = ''
        string += '\n' + 80 * '-' + '\n'
        if hasattr(self, 'name') and self.name is not None:
            string += self.name.upper().center(80) + '\n'
        else:
            string += self.__class__.__name__.upper().center(80) + '\n'
        string += 80 * '-' + '\n\n'
        string += function(*args)
        string += '\n' + 80 * '-' + '\n'
        return string

    return wrapper
