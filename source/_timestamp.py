from datetime import datetime, timezone
from typing import Literal
from colorama import Fore

class Timestamp:
    """
    **Handles creation and formatting of timestamps.**
    
    Description
    
    *Methods*:
    - `get() -> str`: Get the current timestamp.
    - `get_iso() -> str`: Get the current timestamp in ISO format.
    - `set_timezone(timezone:timezone) -> None`: Set the timezone to use in the
    timestamps.
    - `set_format(format:str) -> None`: Set the format of the timestamp.
    - `set_state(state:Literal['enabled', 'disabled']) -> None`: Disable or enable
    timestamps on logging outputs.
    """

    _format = '{HH}:{MI}:{SS}'
    _disabled = False
    _last_timestamp:datetime = None
    _timezone:timezone = None

    # -------------------------------------------
    #  Private Methods
    # -------------------------------------------

    @classmethod
    def _build_timestamp(cls) -> str:
        """
        **Build a timestamp from the current time.**
        
        *Returns*:
        - (str): The current timestamp with the set format applied.
        """

        now = datetime.now(cls._timezone)

        # Extract difference components
        if cls._last_timestamp is None or now.tzname() != cls._last_timestamp.tzname():
            diff_hours = diff_mins = diff_secs = diff_micros = 0
        else:
            diff = now - cls._last_timestamp
            total_secs = diff.total_seconds()
            diff_hours, secs = divmod(total_secs, 60 * 60)
            diff_mins, diff_secs = divmod(secs, 60)
            diff_micros = diff.microseconds // 1000

        # Lookup table for templates
        lookup = {
            '{YY}': f'{now.year:04d}',
            '{MO}': f'{now.month:02d}',
            '{DD}': f'{now.day:02d}',
            '{HH}': f'{now.hour:02d}',
            '{MI}': f'{now.minute:02d}',
            '{SS}': f'{now.second:02d}',
            '{MS}': f'{now.microsecond // 1000:03d}',
            '{DH}': f'{int(diff_hours):02d}',
            '{DM}': f'{int(diff_mins):02d}',
            '{DS}': f'{int(diff_secs):02d}',
            '{DM}': f'{diff_micros:03d}',
        }

        # Format the timestamp
        timestamp = cls._format
        for template, value in lookup.items():
            timestamp = timestamp.replace(template, value)

        cls._last_timestamp = now

        return timestamp

    # -------------------------------------------
    #  Public Methods
    # -------------------------------------------

    @classmethod
    def get(cls) -> str:
        """
        **Get the current timestamp.**
        
        *Returns*:
        - (str): The current timestamp.
        """

        if cls._disabled:
            return ''

        return f'{Fore.MAGENTA}[{cls._build_timestamp()}]{Fore.RESET} '

    @classmethod
    def get_iso(cls) -> str:
        """
        **Get the current timestamp in ISO format.**
        
        *Returns*:
        - (str): The current timestamp in ISO format.
        """

        return datetime.now(tz=cls._timezone).isoformat()

    @classmethod
    def set_timezone(cls, timezone:timezone=None):
        """
        **Set the timezone to use in the timestamps.**
        
        *Parameters*:
        - `timezone` (timezone): Timezone to use, if not omitted, the timezone will be
        the host computers current timezone.
        """

        cls._timezone = timezone

    @classmethod
    def set_format(cls, format:str):
        """
        **Set the format of the timestamp.**
        
        *Parameters*:
        - `format` (str): The timestamp format that is used when getting a timestamp.

        *Templates*:
        - `{YY}` : Year
        - `{MO}` : Month
        - `{DD}` : Day
        - `{HH}` : Hour
        - `{MI}` : Minute
        - `{SS}` : Second
        - `{MS}` : Milliseconds (3 decimals)
        - `{DH}` : Difference hours
        - `{DM}` : Difference minutes
        - `{DS}` : Difference seconds
        - `{DM}` : Difference milliseconds (3 decimals)
        """

        cls._format = format

    @classmethod
    def set_state(cls, state:Literal['enabled', 'disabled']):
        """
        **Disable or enable timestamps on logging outputs.**
        
        *Parameters*:
        - `state` (Literal['enabled', 'disabled']): The new timestamp state.
        """

        cls._disabled = state == 'disabled'
