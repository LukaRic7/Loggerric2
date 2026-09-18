# Loggerric

A logging utility for CLI applications. Offers colorful CLI outputs via ANSI escape characters, aswell as filelogging and a bunch of quality of life features.

---

## Features

- **Logging:** Structured logging with levels `INFO` `WARN` `ERROR` `DEBUG` and highlighting.
- **Filelogging:** Automatic logging to file with ISO timestamps and filepath descriptors.
- **Pretty Printing:** Pretty print different data types with indentation support.
- **Tables:** Print data tables in different styles, handles autosizing of the headers.
- **Progress Bars:** Real-time progressbars with metric labels like ETA, elapsed, etc.
- **Prompts:** Interactive user input with optional choices and default values.
- **Timers:** Measure execution time of code snippets with ease.
- **Timestamps:** Optional, can be used independently, supports rolling differences.
- **Log Manager:** Optional, can be used to disable logging from certain files.

---

## Installation

```
pip install loggerric2
```

**Dependencies:**
```
pip install colorama
```

---

### `Log` class
```py
import loggerric2 as lr2

lr2.Log.info('Output an information message!')
lr2.Log.warn('You can also do warning messages!', highlight='warning')
lr2.Log.error('Here is an error message!', hl='error')
lr2.Log.debug('You can highlight multiple segments!', hl=['highlight', 'segments'])

lr2.Log.disable_level('debug') # Now all debug logs wont be logged to CLI or file.
lr2.Log.enable_level('debug')  # Re-enable the debug logging level again.

lr2.Log.set_log_filepath(path='./logs')  # Make sure to set the filepath before enabling.
lr2.Log.set_filelogging_state('enabled') # Enable filelogging.
```

### `ProgressBar` class
```py
import loggerric2 as lr2

# This will print a progress bar to the CLI.
for i in lr2.ProgressBar(range(100)):
    ...
```

### `Table` class
```py
import loggerric2 as lr2

headers = ('Item Name', 'Quantity', 'Price')
rows = (
    ('Socks', 24, '$2.24'),
    ('Trex', 1, '$12.2M'),
    ('Apple', 912, '$0.54')
)

lr2.Table.minimalistic(headers, rows)
lr2.Table.boxed(headers, rows)
lr2.Table.borderless(headers, rows)
```

### `Timer` class
```py
import loggerric2 as lr2

with Timer(name='Timer Name') as timer:
    ...

duration = timer.get_duration_ms()
duration_f = timer.get_formatted_duration()
```

### `pretty_print` method
```py
import loggerric2 as lr2

lr2.pretty_print([1, 2, 'three', 4.5])

lr2.pp({ 'Key': 'Value', 'Downloads': 123 }) # Exact same as pretty_print, just an alias
```

### `prompt` method
```py
import loggerric2 as lr2

# Prompt without options, just a regular prompt
option = prompt('Question')

# Prompt with options, still accepts other options than specified
option = prompt('Question', options=['Option 1', 'Option 2'])

# Prompt with options, and a default option if user just clicks enter
option = prompt('Question', option=['One', 'Two'], default_option='One')

# Also supports case sensitive options
option = prompt('Question', option=['One', 'Two'], case_sensitive=True)

# And an autocomplete for long options or faster prompting
option = prompt('Question', option=['One', 'Two'], auto_complete_option=True)
```

### `Timestamp` class
```py
import loggerric2 as lr2

lr2.Timestamp.set_timezone(datetime.timezone.utc) # Sets the timezone to use for timestamps.

# Set the format that will be used when getting timestamps
lr2.Timestamp.set_format('{DD}/{MO}/{YY} {HH}:{MI}:{SS}.{MS} T+{DH}:{DM}:{DS}.{DM}')

lr2.Timestamp.get() # Gets the current timestamp with the set format and timezone
lr2.Timestamp.get_iso() # Gets the current ISO timestamp.

lr2.Timestamp.set_state('disabled') # Disable the timestamps on the logs
lr2.Timestamp.set_state('enabled') # Re-enable them again
```

### `LogManager` class
```py
import loggerric2 as lr2

# Get the file of the function that called this method
caller = lr2.LogManager.get_method_caller()

# Get the file that created a class instance
owner = lr2.LogManager.get_class_instance_owner_file()

# Set how many directories of the caller path to show
lr2.LogManager.set_caller_file_depth(2)

# Get the formatted caller filepath
lr2.LogManager.get_caller_file()

# Get the filepath without ANSI formatting
lr2.LogManager.get_caller_file(no_ansi=True)

# Skip additional caller frames
lr2.LogManager.get_caller_file(skip_extra=1)

# Blacklist the current file
lr2.LogManager.blacklist_this_file()

# Remove the current file from the blacklist
lr2.LogManager.remove_this_files_blacklist()

# Check if the current file is blacklisted
lr2.LogManager.is_caller_blacklisted()

# Add a file or path to the blacklist
lr2.LogManager.add_blacklist('debug.py')

# Remove a file or path from the blacklist
lr2.LogManager.blacklist_remove('debug.py')

# Get all blacklisted paths
lr2.LogManager.get_blacklist()

# Check if a specific path is blacklisted
lr2.LogManager.is_blacklisted('debug.py')
```