try:
    from colorama import init
except ImportError:
    print('Package "colorama" not found!')
    exit(1)

from source._timestamp import Timestamp
from source._log_manager import LogManager
from source._timer import Timer
from source._progress_bar import ProgressBar
from source._table import Table
from source._prompt import prompt
from source._pretty_print import pretty_print, pp
from source._log import Log

# Expose functions/classes
__all__ = ['Timestamp', 'LogManager', 'Timer', 'ProgressBar', 'Table', 'prompt',
           'pretty_print', 'pp', 'Log']

# Initialize Colorama
init(autoreset=True)