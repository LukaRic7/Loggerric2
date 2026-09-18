from typing import Literal
from threading import Lock
from colorama import Fore
from pathlib import Path

from loggerric2 import Timestamp, LogManager

class Log:
    """
    **Contains logging methods with level support.**
    
    *Methods*:
    - `disable_level(*levels:Literal['info', 'warn', 'error', 'debug']) -> None`:
    Disable logging levels.
    - `enable_level(*levels:Literal['info', 'warn', 'error', 'debug']) -> None`: Enable
    logging levels.
    - `info(*values, highlight:str|tuple[str], hl:str|tuple[str]) -> None`: Log an
    information level value to the CLI.
    - `warn(*values, highlight:str|tuple[str], hl:str|tuple[str]) -> None`: Log a
    warning level value to the CLI.
    - `error(*values, highlight:str|tuple[str], hl:str|tuple[str]) -> None`: Log an
    error level value to the CLI.
    - `debug(*values, highlight:str|tuple[str], hl:str|tuple[str]) -> None`: Log a debug
    level value to the CLI.
    - `key_value(key, value, key_length:int) -> None`: Output a key value pair to the
    CLI, supports a set key length if printing multiple values.
    - `set_filelogging_state(state:Literal['enabled', 'disabled']) -> None`: Set the
    filelogging state.
    - `set_log_filepath(path:str='./logs', filename:str=None) -> None`: Set the
    filelogging path and optionally the filename.
    """

    _thread_lock = Lock()
    _disabled_levels = set()
    _filelogging_disabled = True
    _filelogging_fulldir_path = None
    _filelogging_name = f'output.log'

    # -------------------------------------------
    #  Private Methods
    # -------------------------------------------

    def _highlight_text(text:str, highlight:str|tuple[str], prefix:str, suffix:str) -> str:
        """
        **Highlight a string using ANSI escape characters.**
        
        *Parameters*:
        - `text` (str): The text to highlight.
        - `highlight` (str|tuple[str]): The part or parts of the text that should be
        highlighted.
        - `prefix` (str): The ANSI escape code to put infront of the highlighted text.
        - `suffix` (str): The ANSI escape code to put behind the highlighted text.
        
        *Returns*:
        - (str): The highlighted text.
        """

        if isinstance(highlight, str):
            highlight = (highlight,)

        for h in highlight:
            text = text.replace(h, prefix + h + suffix, 1)

        return text

    @classmethod
    def _log2file(cls, content:str):
        """
        **Log the given content to the logging file.**
        
        *Parameters*:
        - `content` (str): The content to log.
        """

        filepath = f'{cls._filelogging_fulldir_path}/{cls._filelogging_name}'
        ts = Timestamp.get_iso()
        caller = LogManager.get_caller_file(no_ansi=True)
        with open(filepath, 'a') as file:
            file.write(f'[{ts}] {caller}{content}\n')

    # -------------------------------------------
    #  Public Methods
    # -------------------------------------------

    @classmethod
    def disable_level(cls, *levels:Literal['info', 'warn', 'error', 'debug']):
        """
        **Disable logging levels.**
        
        *Parameters*:
        - `*levels` (Literal['info', 'warn', 'error', 'debug']): The levels to block.
        """

        for level in levels:
            cls._disabled_levels.add(level)

    @classmethod
    def enable_level(cls, *levels:Literal['info', 'warn', 'error', 'debug']):
        """
        **Enable logging levels.**
        
        *Parameters*:
        - `*levels` (Literal['info', 'warn', 'error', 'debug']): The levels to enable.
        """

        for level in levels:
            cls._disabled_levels.remove(level)

    @classmethod
    def info(cls, *values, highlight:str|tuple[str]=None, hl:str|tuple[str]=None):
        """
        **Log an information level value to the CLI.**
        
        *Parameters*:
        - `*values` (any): The values to print.
        - `highlight` (str|tuple[str]): The part or parts of text to highlight in the
        given values.
        - `hl` (str|tuple[str]): Does the exact same as the `highlight` but is just a
        shorter argument.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return
        if 'info' in cls._disabled_levels: return

        string = ' '.join(values)
        string_f = string

        hl = hl or highlight
        if hl:
            string_f = cls._highlight_text(string, hl, Fore.YELLOW, Fore.GREEN)

        with cls._thread_lock:
            print(Timestamp.get() + LogManager.get_caller_file()
                + f'{Fore.GREEN}[i] {string_f}{Fore.RESET}')

            if not cls._filelogging_disabled:
                cls._log2file(f'[i] {string}')

    @classmethod
    def warn(cls, *values, highlight:str|tuple[str]=None, hl:str|tuple[str]=None):
        """
        **Log a warning level value to the CLI.**
        
        *Parameters*:
        - `*values` (any): The values to print.
        - `highlight` (str|tuple[str]): The part or parts of text to highlight in the
        given values.
        - `hl` (str|tuple[str]): Does the exact same as the `highlight` but is just a
        shorter argument.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return
        if 'warn' in cls._disabled_levels: return

        string = ' '.join(values)
        string_f = string

        hl = hl or highlight
        if hl:
            string_f = cls._highlight_text(string, hl, Fore.WHITE, Fore.YELLOW)

        with cls._thread_lock:
            print(Timestamp.get() + LogManager.get_caller_file()
                + f'{Fore.YELLOW}[w] {string_f}{Fore.RESET}')

            if not cls._filelogging_disabled:
                cls._log2file(f'[w] {string}')

    @classmethod
    def error(cls, *values, highlight:str|tuple[str]=None, hl:str|tuple[str]=None):
        """
        **Log an error level value to the CLI.**
        
        *Parameters*:
        - `*values` (any): The values to print.
        - `highlight` (str|tuple[str]): The part or parts of text to highlight in the
        given values.
        - `hl` (str|tuple[str]): Does the exact same as the `highlight` but is just a
        shorter argument.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return
        if 'error' in cls._disabled_levels: return

        string = ' '.join(values)
        string_f = string

        hl = hl or highlight
        if hl:
            string_f = cls._highlight_text(string, hl, Fore.YELLOW, Fore.RED)

        with cls._thread_lock:
            print(Timestamp.get() + LogManager.get_caller_file()
                + f'{Fore.RED}[!] {string_f}{Fore.RESET}')

            if not cls._filelogging_disabled:
                cls._log2file(f'[!] {string}')

    @classmethod
    def debug(cls, *values, highlight:str|tuple[str]=None, hl:str|tuple[str]=None):
        """
        **Log a debug level value to the CLI.**
        
        *Parameters*:
        - `*values` (any): The values to print.
        - `highlight` (str|tuple[str]): The part or parts of text to highlight in the
        given values.
        - `hl` (str|tuple[str]): Does the exact same as the `highlight` but is just a
        shorter argument.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return
        if 'debug' in cls._disabled_levels: return

        string = ' '.join(values)
        string_f = string

        hl = hl or highlight
        if hl:
            string_f = cls._highlight_text(string, hl, Fore.YELLOW, Fore.LIGHTBLACK_EX)

        with cls._thread_lock:
            print(Timestamp.get() + LogManager.get_caller_file()
                + f'{Fore.LIGHTBLACK_EX}[-] {string_f}{Fore.RESET}')

            if not cls._filelogging_disabled:
                cls._log2file(f'[-] {string}')

    @classmethod
    def key_value(cls, key, value, key_length:int=20):
        """
        **Output a key value pair to the CLI, supports a set key length if printing
        multiple values.**
        
        *Parameters*:
        - `key` (any): The key part of the text.
        - `value` (any): The value part of the text.
        - `key_length` (int): The length of the key.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return

        key, value = str(key), str(value)

        key = key + ('.' * (key_length - len(key)))
        print(Timestamp.get() + LogManager.get_caller_file()
              + f'{Fore.GREEN}{key}: {Fore.YELLOW}{value}{Fore.RESET}')

    @classmethod
    def set_filelogging_state(cls, state:Literal['enabled', 'disabled']):
        """
        **Set the filelogging state.**
        
        *Parameters*:
        - `state` (Literal['enabled', 'disabled']): If enabled, the logging methods will
        also be outputted in an understandable and timezone aware format to a log file.
        """

        cls._filelogging_disabled = state == 'disabled'

        if cls._filelogging_disabled == False and cls._filelogging_fulldir_path == None:
            print(f'{Fore.RED}Filelogging location is not set, call '
                  + f'{Fore.YELLOW}set_log_filepath()'
                  + f'{Fore.RED} to specify a location.{Fore.RESET}')

    @classmethod
    def set_log_filepath(cls, path:str='./logs', filename:str=None):
        """
        **Set the filelogging path and optionally the filename.**
        
        *Parameters*:
        - `path` (str): The path that the logfiles will be in. Defaults to a logs/
        folder in the parent directory of the caller.
        - `filename` (str): The filename of the log, if not omitted it will
        automatically set it's extension to .log
        """

        caller = Path(LogManager.get_method_caller())

        log_path = Path(path)
        if not log_path.is_absolute():
            log_path = caller.parent / log_path

        log_path.mkdir(parents=True, exist_ok=True)

        cls._filelogging_fulldir_path = str(log_path)

        if filename:
            filename = filename if filename.endswith('.log') else filename + '.log'
            cls._filelogging_name = filename
