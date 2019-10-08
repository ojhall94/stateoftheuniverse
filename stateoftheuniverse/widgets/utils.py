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

    Example:
        In you widget, the signature the the get_string() method
        should look like the following:
        ```
        @stringdecorator
        def get_string(self):
            ...
            return string
        ```
        This will make the output of get_string() to look like this:
        ```
        ----------------------------------------------------------------
            WIDGET NAME (given by self.name in widget constructor)
        ----------------------------------------------------------------

        Widget output (i.e., the original string from get_string()).

        ----------------------------------------------------------------
        ```

    Args:
        function: The function to be decorated. Generally, this will
            be the `get_string()` method of a widget.

    Returns:
        The decorated `function`.
    """

    def wrapper(*args):
        self = args[0]
        string = ''
        string += '<br>' + 80 * '-' + '<br>'
        if hasattr(self, 'name') and self.name is not None:
            string += self.name.upper().center(80) + '<br>'
        else:
            string += self.__class__.__name__.upper().center(80) + '<br>'
        string += 80 * '-' + '<br><br>'
        string += function(*args)
        string += '<br>' + 80 * '-' + '<br>'
        return string

    return wrapper
