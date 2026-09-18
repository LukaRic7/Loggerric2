from colorama import Fore
from pathlib import Path
import inspect

class LogManager:
    """
    **Handles getting and formatting of the caller file.**
    
    *Methods*:
    - `get_method_caller() -> str`: Get the file of the function or method that called
    this method.
    - `get_class_instance_owner_file() -> str`: Called from inside class init to find
    out what file created a the instance.
    - `set_caller_file_depth(depth:int) -> None`: Set the caller file path directory
    depth when getting the caller file.
    - `get_caller_file(no_ansi:bool) -> str`: Get the formatted caller filepath using
    the set depth.
    - `blacklist_this_file() -> None`: Blacklist the file calling this function.
    - `remove_this_files_blacklist() -> None`: Remove the caller file from the
    blacklist.
    - `is_caller_blacklisted() -> bool`: Checks if the caller file is blacklisted.
    - `add_blacklist(path:str) -> None`: Add the path to the blacklist.
    - `blacklist_remove(path:str) -> None`: Remove the path from the blacklist.
    - `get_blacklist() -> list[str]`: Get the current blacklisted paths.
    - `is_blacklisted(path:str) -> bool`: Check if a path is blacklisted.
    """

    _blacklisted_paths = set()
    _caller_file_depth = 2
    _ignored_paths = { Path(__file__).resolve().parent, }

    # -------------------------------------------
    #  Private Methods
    # -------------------------------------------

    @classmethod
    def _get_caller_path(cls, skip_extra:int=0) -> Path|None:
        """
        **Gets the caller file as a Path object from pathlib.**
        
        *Parameters*:
        - `skip_extra` (int): The extra skips to make.

        *Returns*:
        - (Path|None): The caller files path it exists in the frame stack.
        """

        frame = inspect.currentframe()

        try:
            skipped = 0
            while frame is not None:
                filename = frame.f_code.co_filename

                # Skip Python internal/frozen files
                if filename.startswith('<'):
                    frame = frame.f_back
                    continue

                caller_file = Path(filename).resolve()

                # Check if file matches or resides inside any ignored path
                is_internal = any(
                    caller_file == ignored or ignored in caller_file.parents
                    for ignored in cls._ignored_paths
                )

                if not is_internal:
                    if skipped < skip_extra:
                        skipped += 1
                    else:
                        return caller_file

                frame = frame.f_back
        finally:
            del frame  # Prevents reference cycles in frame stack

        return None

    @classmethod
    def _is_path_blacklisted(cls, path:str|Path) -> bool:
        """
        **Checks if a path is blacklisted.**
        
        *Parameters*:
        - `path` (str|Path): The path to check.
        
        *Returns*:
        - (bool): True if the given path is blacklisted.
        """

        path = Path(path).resolve()
        path_parts = [part.lower() for part in path.parts]

        for blacklist_path in cls._blacklisted_paths:
            supplied = Path(str(blacklist_path).replace('\\', '/'))
            supplied_parts = [part.lower() for part in supplied.parts]

            # Filename or directory name
            if len(supplied_parts) == 1:
                if path.name.lower() == supplied_parts[0]:
                    return True

                if supplied_parts[0] in path_parts[:-1]:
                    return True

            # Path fragment
            elif len(supplied_parts) <= len(path_parts):
                if path_parts[-len(supplied_parts):] == supplied_parts:
                    return True

        return False

    @classmethod
    def _path_matches(cls, path:str|Path, blacklist_path:str|Path) -> bool:
        """
        **Check if a path matches a blacklisted path.**
        
        *Parameters*:
        - `path` (str|Path): The first path.
        - `blacklist_path` (str|Path): The second path.
        
        *Returns*:
        - (bool): True if the paths matches.
        """

        path = Path(str(path).replace('\\', '/'))
        blacklist_path = Path(str(blacklist_path).replace('\\', '/'))

        path_parts = [part.lower() for part in path.parts]
        blacklist_parts = [part.lower() for part in blacklist_path.parts]

        if len(path_parts) == 1:
            return path_parts[0] == blacklist_parts[-1]
        
        if len(path_parts) <= len(blacklist_parts):
            return blacklist_parts[-len(path_parts):] == path_parts

        return False

    # -------------------------------------------
    #  Public Methods
    # -------------------------------------------

    @staticmethod
    def get_method_caller() -> str:
        """
        **Get the file of the function or method that called this method.**
        
        *Returns*:
        - (str): The filepath of the method/function caller.
        """

        frame = inspect.currentframe()

        try:
            method = frame.f_back
            if method is None: return

            caller = method.f_back
            if caller is None: return

            return caller.f_code.co_filename
        finally:
            del frame

    @staticmethod
    def get_class_instance_owner_file() -> str:
        """
        **Called from inside class init to find out what file created a the instance.**

        *Returns*:
        - (str): Instantiator file path.
        """

        frame = inspect.currentframe()

        try:
            return frame.f_back.f_back.f_code.co_filename
        finally:
            del frame

    @classmethod
    def set_caller_file_depth(cls, depth:int):
        """
        **Set the caller file path directory depth when getting the caller file.**
        
        *Parameters*:
        - `depth` (int): The depth to return.
        """

        cls._caller_file_depth = max(1, depth)

    @classmethod
    def get_caller_file(cls, no_ansi:bool=False, skip_extra:int=0) -> str:
        """
        **Get the formatted caller filepath using the set depth.**
        
        *Parameters*:
        - `no_ansi` (bool): Disable ANSI color formatting.
        - `skip_extra` (int): Optional number of external frames to skip further.
        
        *Returns*:
        - (str): The formatted caller file with ANSI.
        """

        caller_file = cls._get_caller_path(skip_extra=skip_extra)
        if caller_file is None:
            return None

        segments = str(caller_file).split('\\')
        path = '\\'.join(segments[max(0, len(segments) - cls._caller_file_depth):])

        if no_ansi:
            return f'<{path}> '
        else:
            return f'{Fore.MAGENTA}<{path}>{Fore.RESET} '

    @classmethod
    def blacklist_this_file(cls):
        """
        **Blacklist the file calling this function.**
        """

        caller_file = cls._get_caller_path()
        if caller_file is None: return

        cls._blacklisted_paths.add(str(caller_file))

    @classmethod
    def remove_this_files_blacklist(cls):
        """
        **Remove the caller file from the blacklist.**
        """

        caller_file = cls._get_caller_path()
        if caller_file is None: return

        cls._blacklisted_paths.remove(str(caller_file))

    @classmethod
    def is_caller_blacklisted(cls) -> bool:
        """
        **Checks if the caller file is blacklisted.**
        
        *Returns*:
        - (bool): True of the caller file is blacklisted.
        """

        caller_file = cls._get_caller_path()

        if caller_file is None:
            return False

        return cls._is_path_blacklisted(caller_file)

    @classmethod
    def add_blacklist(cls, path:str):
        """
        **Add the path to the blacklist.**
        
        *Parameters*:
        - `path` (str): The path to blacklist.
        """

        cls._blacklisted_paths.add(path)

    @classmethod
    def blacklist_remove(cls, path:str):
        """
        **Remove the path from the blacklist.**
        
        *Parameters*:
        - `path` (str): The path to remove from blacklist.
        """

        cls._blacklisted_paths.remove(path)

    @classmethod
    def get_blacklist(cls) -> list[str]:
        """
        **Get the current blacklisted paths.**
        
        *Returns*:
        - (list[str]): A list of the blacklisted paths.
        """

        return list(cls._blacklisted_paths)

    @classmethod
    def is_blacklisted(cls, path:str|Path) -> bool:
        """
        **Check if a path is blacklisted.**
        
        *Parameters*:
        - `path` (str|Path): The path to check.
        
        *Returns*:
        - (bool): True if the path is blacklisted.
        """

        for blacklist_path in cls._blacklisted_paths:
            if cls._path_matches(path, blacklist_path):
                return True

        return False
