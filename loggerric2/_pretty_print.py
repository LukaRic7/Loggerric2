from colorama import Fore

from loggerric2 import Timestamp, LogManager

# -------------------------------------------
#  Private Methods
# -------------------------------------------

def _format_obj(obj, depth:int=0, minify_length_limit:int=25, indent_size:int=4) -> str:
    """
    **Recursive helper function to format objects with color and indentation.**
    
    *Parameters*:
    - `obj` (any): The object to format.
    - `depth` (int): The current depth.
    - `minify_length_limit` (int): The length an object has to be under to be minified.
    - `indent_size` (int): The amount of space characters a layer of indentation is.
    
    *Returns*:
    - (str): The formatted object.
    """
    
    indent_str = ' ' * indent_size
    current_indent = indent_str * depth
    next_indent = indent_str * (depth + 1)
    
    # Strings (GREEN, wrapped in "")
    if isinstance(obj, str):
        return f'{Fore.GREEN}"{obj}"{Fore.RESET}'
        
    # Booleans (CYAN) - check before int because bool is a subclass of int
    elif isinstance(obj, bool):
        return f'{Fore.CYAN}{obj}{Fore.RESET}'
        
    # Integers and Floats (CYAN)
    elif isinstance(obj, (int, float)):
        return f'{Fore.CYAN}{obj}{Fore.RESET}'
        
    # Dictionaries (BLUE brackets, recursive content)
    elif isinstance(obj, dict):
        open_b = f'{Fore.BLUE}{{{Fore.RESET}'
        close_b = f'{Fore.BLUE}}}{Fore.RESET}'
        
        if not obj:
            return f"{open_b}{close_b}"
            
        # Minified dictionary check
        if len(str(obj)) <= minify_length_limit:
            inner = ", ".join(f"{_format_obj(k, 0)}: {_format_obj(v, 0)}"
                              for k, v in obj.items())
            return f"{open_b} {inner} {close_b}"
        else:
            lines = [f"{next_indent}{_format_obj(k, depth + 1)}: {_format_obj(v, depth + 1)}"
                     for k, v in obj.items()]
            return f"{open_b}\n{',\n'.join(lines)}\n{current_indent}{close_b}"

    # Lists, Sets, Tuples, Frozensets (BLUE brackets, recursive content)
    elif isinstance(obj, (list, set, tuple, frozenset)):
        if isinstance(obj, list):
            b_open, b_close = '[', ']'
        elif isinstance(obj, tuple):
            b_open, b_close = '(', ')'
        elif isinstance(obj, set):
            b_open, b_close = '{', '}'
        else: # frozenset
            b_open, b_close = 'frozenset({', '})'
            
        open_b = f'{Fore.BLUE}{b_open}{Fore.RESET}'
        close_b = f'{Fore.BLUE}{b_close}{Fore.RESET}'
        
        if not obj:
            return f"{open_b}{close_b}"
            
        # Minified list/set/tuple check
        if len(str(obj)) <= minify_length_limit:
            inner = ", ".join(_format_obj(item, 0) for item in obj)
            return f"{open_b} {inner} {close_b}"
        else:
            lines = [f"{next_indent}{_format_obj(item, depth + 1)}" for item in obj]
            return f"{open_b}\n{',\n'.join(lines)}\n{current_indent}{close_b}"
            
    # Any other object, classes, methods (WHITE str(obj))
    else:
        return f'{Fore.WHITE}{str(obj)}{Fore.RESET}'

# -------------------------------------------
#  Public Methods
# -------------------------------------------

def pretty_print(object, **kwargs):
    """
    **Pretty print any object to the console, supports indentation.**
    
    *Parameters*:
    - `object` (any): The object to pretty print.
    """

    if LogManager.is_blacklisted(LogManager.get_method_caller()): return

    # Extract formatting parameters from kwargs
    depth = kwargs.get('depth', 0)
    is_first_line = kwargs.get('is_first_line', True)

    if is_first_line:
        # Print header info on the first printed line
        print(str(Timestamp.get()) + str(LogManager.get_caller_file()))

    # Print the recursively formatted object
    print(_format_obj(object, depth))

def pp(object):
    """
    **Pretty print any object to the console, supports indentation.**

    *Parameters*:
    - `object` (any): The object to pretty print.
    """

    pretty_print(object)
