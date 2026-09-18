from time import perf_counter
from typing import Iterable
from colorama import Fore
import math

from source import Timestamp, LogManager

class ProgressBar:
    """
    **Creates a progressbar when wrapped around an iterator.**
    
    Big iterators will have fewer updates as to not slow down the program.

    *Methods*:
    - `rename(new_name) -> None`: Rename the progressbar.
    - `update(current_index) -> None`: Updates the progressbar in the console.
    """

    def __init__(self, iterable:Iterable, name:str='Progress', bar_length:int=30,
                 percent_complete:bool=True, progress_line:bool=True,
                 estimated_time_left:bool=True, elapsed_time:bool=False,
                 fraction:bool=False, amount_left:bool=False):
        """
        *Parameters*:
        - `iterable` (Iterable): The iterable to iterate and display a progress for.
        - `name` (str): The name of the progress. Can be changed during iteration.
        - `bar_length` (int): The length of the progress bar line segment.
        - `percent_complete` (bool): If true, shows the percentage until complete with 1
        decimal place.
        - `progress_line` (bool): If true, shows the progressbar line.
        - `estimated_time_left` (bool): If true, shows the estimated time left until
        completion.
        - `amount_left` (bool): If true, shows the amount of iterations left until
        completion.
        - `fraction` (bool): If true, shows the iterations completed out of the total
        amount of iterations to be made.
        - `elapsed_time` (bool): If true, shows the elapsed time since the start of
        iteration.
        """

        self._iterable = iterable
        self._name = name
        self._bar_length = bar_length

        self._end_index = len(iterable)
        self._start_time = None
        self._current_index = 0
        self._longest_name_len = len(self._name)

        self._percent_complete = percent_complete
        self._progress_line = progress_line
        self._estimated_time_left = estimated_time_left
        self._elapsed_time = elapsed_time
        self._fraction = fraction
        self._amount_left = amount_left

        self._instance_owner_file = LogManager.get_class_instance_owner_file()

    def __iter__(self):
        self._start_time = perf_counter()

        update_every = math.floor(self._end_index / 1000)

        for item in self._iterable:
            self._current_index += 1

            if update_every <= 1 or self._current_index % update_every == 0:
                self.update(self._current_index)

            yield item

    # -------------------------------------------
    #  Private Methods
    # -------------------------------------------

    def _format_time(self, seconds:int) -> str:
        """
        **Format time from seconds to hours, minutes and seconds.**
        
        *Parameters*:
        - `seconds` (int): The amount seconds to format.
        
        *Returns*:
        - (str): The formatted time in HH:MM:SS format.
        """

        hours, secs = divmod(seconds, 60 * 60)
        mins, secs = divmod(secs, 60)

        return f'{min(99, hours):02d}:{mins:02d}:{secs:02d}'

    def _build_percent_complete(self, current_index:int) -> str:
        """
        **Build the percentage complete string.**
        
        *Parameters*:
        - `current_index` (int): The current index of the iteration.
        
        *Returns*:
        - (str): The complete percentage.
        """

        return f'{Fore.CYAN}{(current_index * 100) / self._end_index:.1f}%{Fore.RESET}'

    def _build_progress_line(self, current_index:int) -> str:
        """
        **Build the progress line.**
        
        *Parameters*:
        - `current_index` (int): The current index the iteration is at.
        
        *Returns*:
        - (str): The progress line.
        """

        progress = current_index * self._bar_length / self._end_index

        done = '#' * math.floor(progress)
        left = '_' * (self._bar_length - math.floor(progress))

        return f'{Fore.BLUE}[{Fore.CYAN}{done}{left}{Fore.BLUE}]{Fore.RESET}'

    def _build_estimated_time_left(self, current_index:int) -> str:
        """
        **Build the ETA time string.**
        
        *Parameters*:
        - `current_index` (int): The current index of the iteration.
        
        *Returns*:
        - (str): The ETA string with formatted time.
        """

        elapsed = perf_counter() - self._start_time
        remaining = (elapsed / current_index) * (self._end_index - current_index)
        return f'{Fore.BLUE}ETA: {Fore.CYAN}{self._format_time(int(remaining))}{Fore.RESET}'

    def _build_elapsed_time(self) -> str:
        """
        **Build the elapsed time string.**
        
        *Returns*:
        - (str): The formatted elapsed time.
        """

        elapsed = perf_counter() - self._start_time
        return f'{Fore.BLUE}ET: {Fore.CYAN}{self._format_time(int(elapsed))}{Fore.RESET}'
    
    def _build_amount_left(self, current_index:int) -> str:
        """
        **Build the amount left string.**
        
        *Parameters*:
        - `current_index` (int): The current index of the iteration.
        
        *Returns*:
        - (str): The formatted amount left string.
        """
        
        remaining = self._end_index - current_index
        return f'{Fore.BLUE}Remaining: {Fore.CYAN}{remaining:,}{Fore.RESET}'

    def _build_fraction(self, current_index:int) -> str:
        """
        **Build the fraction string.**
        
        *Parameters*:
        - `current_index` (int): The current index of the iteration.
        
        *Returns*:
        - (str): The formatted fraction string.
        """

        return (f'{Fore.BLUE}[{Fore.CYAN}{current_index:,}{Fore.BLUE}'
                + f'/{Fore.CYAN}{self._end_index:,}{Fore.BLUE}]{Fore.RESET}')

    # -------------------------------------------
    #  Public Methods
    # -------------------------------------------

    def rename(self, new_name:str):
        """
        **Rename the progressbar.**
        
        *Parameters*:
        - `new_name` (str): The new name for the progressbar.
        """

        self._name = new_name
        self._longest_name_len = max(len(new_name), self._longest_name_len)

    def update(self, current_index:int):
        """
        **Updates the progressbar in the console.**
        
        *Parameters*:
        - `current_index` (int): The index the progress is at.
        """

        ts = Timestamp.get()
        caller = LogManager.get_caller_file()

        progress_bar = f'{ts}{caller}{Fore.BLUE}{self._name}:'
        max_len = self._longest_name_len + 1

        if self._percent_complete:
            progress_bar += ' ' + self._build_percent_complete(current_index)
            max_len += 7
        if self._progress_line:
            progress_bar += ' ' + self._build_progress_line(current_index)
            max_len += self._bar_length + 3
        if self._estimated_time_left:
            progress_bar += ' ' + self._build_estimated_time_left(current_index)
            max_len += 14
        if self._elapsed_time:
            progress_bar += ' ' + self._build_elapsed_time()
            max_len += 12
        if self._amount_left:
            progress_bar += ' ' + self._build_amount_left(current_index)
            max_len += len(f'{self._end_index - current_index:,}') + 11
        if self._fraction:
            progress_bar += ' ' + self._build_fraction(current_index)
            max_len += len(f'{current_index:,}') + len(f'{self._end_index:,}') + 3

        if not LogManager.is_blacklisted(self._instance_owner_file):
            print(progress_bar + (' ' * (max_len - len(progress_bar))), end='\r')

        if current_index == self._end_index:
            print()
