try:
    from colorama import init
except ImportError:
    print('Package "colorama" not found!')
    exit(1)

from loggerric2._timestamp import Timestamp
from loggerric2._log_manager import LogManager
from loggerric2._timer import Timer
from loggerric2._progress_bar import ProgressBar
from loggerric2._table import Table
from loggerric2._prompt import prompt
from loggerric2._pretty_print import pretty_print, pp
from loggerric2._log import Log

def get_version() -> str:
    """
    **Get the current Loggerric2 version.**

    *Returns*:
    - (str): The current version, using Major.Minor.Patch format.
    """

    return '1.1.0'

# Expose functions/classes
__all__ = ['Timestamp', 'LogManager', 'Timer', 'ProgressBar', 'Table', 'prompt',
           'pretty_print', 'pp', 'Log', 'get_version']

# Initialize Colorama
init(autoreset=True)
