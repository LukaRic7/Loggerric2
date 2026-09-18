from types import TracebackType
from time import perf_counter
from colorama import Fore

from loggerric2 import Timestamp, LogManager

class Timer:
    """
    **Creates a timer, use the `with` operator to start timing.**
    
    *Methods*:
    - `get_formatted_duration() -> str`: Get the formatted duration that the timer ran
    for.
    - `get_duration_ms() -> float`: Get the duration the timer ran for in milliseconds.
    """

    def __init__(self, name:str='Timer'):
        """
        *Parameters*:
        - `name` (str): The displayed name of the timer.
        """

        self._name = name

        self._instance_owner_file = LogManager.get_class_instance_owner_file()
    
    def __enter__(self):
        if not LogManager.is_blacklisted(self._instance_owner_file):
            # Log the start of the timer
            print(f'{Timestamp.get()}{LogManager.get_caller_file()}'
                  + f'{Fore.BLUE}{self._name}: {Fore.CYAN}Started...{Fore.RESET}')

        self._start = perf_counter()
        self._duration_ms = 0.0

        return self

    def __exit__(self, exc_type:BaseException|None, exc_value:BaseException|None,
                 traceback:TracebackType|None):
        self._duration_ms = (perf_counter() - self._start) * 1000

        if not LogManager.is_blacklisted(self._instance_owner_file):
            # Log the timer completion
            elapsed = self.get_formatted_duration()
            print(f'{Timestamp.get()}{LogManager.get_caller_file()}'
                  + f'{Fore.BLUE}{self._name}: {Fore.CYAN}Finished! '
                  + f'{Fore.YELLOW}{elapsed} {Fore.CYAN}Elapsed.{Fore.RESET}')

    # -------------------------------------------
    #  Private Methods
    # -------------------------------------------

    def _format_duration(self, duration_ms:float) -> str:
        """
        **Format milliseconds into hours, minutes, seconds and milliseconds.**
        
        *Parameters*:
        - `duration_ms` (float): The duration to format in milliseconds.
        
        *Returns*:
        - (str): The formatted duration.
        """

        # Convert input ms to: hours, mins, secs, ms
        hours, millis = divmod(duration_ms, 1000 * 60 * 60)
        mins, millis = divmod(millis, 1000 * 60)
        secs, millis = divmod(millis, 1000)

        # Return only the nessessary units
        if duration_ms >= 1000 * 60 * 60:
            return f'{hours:.0f}h {mins:.0f}m {secs:.0f}s {millis:.5f}ms'
        elif duration_ms >= 1000 * 60:
            return f'{mins:.0f}m {secs:.0f}s {millis:.5f}ms'
        elif duration_ms >= 1000:
            return f'{secs:.0f}s {millis:.5f}ms'
        else:
            return f'{millis:.5f}ms'

    # -------------------------------------------
    #  Public Methods
    # -------------------------------------------

    def get_formatted_duration(self) -> str:
        """
        **Get the formatted duration that the timer ran for.**

        *Returns*:
        - (str): The formatted duration.
        """

        return self._format_duration(self._duration_ms)

    def get_duration_ms(self) -> float:
        """
        **Get the duration the timer ran for in milliseconds.**
        
        If used inside the `with` operator, this will return 0.0
        
        *Returns*:
        - (float): The duration in milliseconds.
        """

        return self._duration_ms
